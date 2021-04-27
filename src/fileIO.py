import json


def loadTask():
  
    with open('Tasks.db', 'r') as f:
        ListOfData = json.load(f)
    return ListOfData
    


def saveTask(ListOfData):
    if ListOfData:
        with open('Tasks.db', 'w') as f:
            json.dump(ListOfData, f)
