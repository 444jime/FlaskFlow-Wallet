import json


def openFile(route):
    with open(route,"r") as f:
        return json.loads(f.read())

def addtofile(route,new_data):
    with open(route,"r") as f:
        data = json.load(f)

    data.update(new_data)

    with open(route,"w") as f:
        json.dump(data,f,indent=4)
    