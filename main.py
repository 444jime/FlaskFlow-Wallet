from flask import Flask,render_template,request,redirect,session,send_from_directory
from business.logic import checkUserPass, accExists
from data.datahelper import openFile, addtofile
import os
import dotenv

dotenv.load_dotenv()
app = Flask(__name__,
            template_folder="./presentation/templates", 
            static_folder="./presentation/static")
app.secret_key = os.getenv("COOKIES_SECRET_KEY")   

@app.route("/",methods = ['GET','POST'])
def index():
    error = False    
    texts = openFile("./presentation/i18n/textsEng.json")
    text = texts["login"]

    if request.method == 'GET':
        return render_template("login.html",error=error,text=text)
    
    if request.method == 'POST':
        user = request.form["username"]
        pwd = request.form["password"]
        
        if checkUserPass(user,pwd) == True:
            session['logged_in'] = True
            session['user'] = user
            return redirect("/welcome")
        else:
            error = True
            return render_template("login.html",error=error,text=text)

@app.route("/welcome",methods = ['GET'])
def welcome():
    texts = openFile("./presentation/i18n/textsEng.json")
    text = texts["welcome"]
    try:
        if session['logged_in'] == True:
            welcomeText =  session['user']
            accounts = openFile("data/accounts.json")
            return render_template("welcome.html",welcomeText=welcomeText,accounts=accounts,text=text)            
        else:
            return redirect("/")
    except KeyError:
        return redirect("/")

@app.route("/logout",methods = ['GET'])
def logout():
    session['logged_in'] = False
    return redirect("/")

@app.route("/createAcc", methods = ['GET','POST'])
def createacc():
    texts = openFile("./presentation/i18n/textsEng.json")
    text = texts["createAcc"]

    rates = openFile("./data/rates.json")

    if request.method== 'GET':
        return render_template("createAcc.html",rates=rates,text=text)
    
    if request.method == 'POST':
        rate = request.form["moneda"]
        mensaje = ""
        tipo_mensaje = ""
        if accExists(rate):
            mensaje = text["error"]
            tipo_mensaje = "error"
        else:
            addtofile("./data/accounts.json",{rate: 0.00})
            mensaje = text["okey"]
            tipo_mensaje = "success"
        return render_template("createAcc.html",rates=rates,mensaje=mensaje,text=text,tipo_mensaje=tipo_mensaje)

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        app.static_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon'
    )
if __name__ == '__main__':
    app.run(debug=True,host='localhost',port = 8000)