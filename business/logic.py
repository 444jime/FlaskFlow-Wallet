import os
from data.datahelper import openFile
from dotenv import load_dotenv

load_dotenv()

def checkUserPass(user,pwd):
    if user == "tbal" and pwd == os.getenv("PWD"):
        return True
    else:
        return False
    
def accExists(acc):
    accs = openFile("data/accounts.json")
    return acc in accs