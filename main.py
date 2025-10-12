from flask import Flask,render_template,request,redirect,session,send_from_directory
from business.logic import checkUserPass, accExists
from data.datahelper import openFile, addtofile
import os
import dotenv
import json

dotenv.load_dotenv()
app = Flask(__name__,
            template_folder="./presentation/templates", 
            static_folder="./presentation/static")
app.secret_key = os.getenv("COOKIES_SECRET_KEY")   

@app.route("/",methods = ['GET','POST'])
def index():
    error = False    
    text = openFile("./presentation/i18n/textsEsp.json")

    if request.method == 'GET':
        return render_template("login.html",error=error,text=text)
    if request.method == 'POST':
        user = request.form["username"]
        pwd = request.form["password"]
        if checkUserPass(user,pwd) == True:
            session['logged_in'] = True
            session['user'] = user
            return redirect("/welcome",text=text)
        else:
            error = True
            return render_template("login.html",error=error,text=text)

@app.route("/welcome",methods = ['GET'])
def welcome():
    try:
        if session['logged_in'] == True:
            welcomeText =  session['user']
            accounts = openFile("data/accounts.json")
            return render_template("welcome.html",welcomeText=welcomeText,accounts=accounts)
            
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
    rates = openFile("./data/rates.json")
    if request.method== 'GET':
        return render_template("createAcc.html",rates=rates)
    if request.method == 'POST':
        rate = request.form["moneda"]
        mensaje = ""
        if accExists(rate):
            mensaje = "Cuenta existente, ingrese otra."
        else:
            addtofile("./data/accounts.json",{rate: 0.00})
            mensaje = "Cuenta creada correctamente"
        return render_template("createAcc.html",rates=rates,moneda=rate, mensaje=mensaje)

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        app.static_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon'
    )
if __name__ == '__main__':
    app.run(debug=True,host='localhost',port = 8000)
