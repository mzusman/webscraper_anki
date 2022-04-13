import requests
import json

def updateByID(id,fields):
    data = {
        "action":"updateNoteFields",
        "version":6,
        "params":{
            "note":{
                "id": id,
                "fields":fields
                            }
        }
        }
    return json.loads(requests.post("http://127.0.0.1:8765", data=json.dumps(data)).content)["result"]


def noteInfosByRegex(regex):
    a = findNotes(regex)
    if len(a) > 0 : 
        return noteInfoByIDs(a)
    return []

def noteInfoByID(id):
    data = {
    "action":"notesInfo",
    "version":6,
    "params":{
        "notes":[id]
        }
    }
    return json.loads(requests.post("http://127.0.0.1:8765", data=json.dumps(data)).content)["result"]


def noteInfoByIDs(array_of_ids):
    infos = []
    for id in array_of_ids:
        data = {
        "action":"notesInfo",
        "version":6,
        "params":{
            "notes":[id]
            }
        }
        infos.append((id,json.loads(requests.post("http://127.0.0.1:8765", data=json.dumps(data)).content)["result"]))
    return infos


def findNotes(regex):
    data = {
        "action":"findNotes",
        "version":6,
        "params":{
            "query":regex
        }
    }
    results = requests.post("http://127.0.0.1:8765", data=json.dumps(data))
    return json.loads(results.content)["result"]

def addNote(deck_name, model_name, fields):
    data = {
        "params": {
            "notes": [
                {
                    "deckName": deck_name,
                    "modelName": model_name,
                    "fields": fields,
                }
            ]
        }
    }
    data["action"] = "canAddNotes"
    results = requests.post("http://127.0.0.1:8765", data=json.dumps(data))
    data["action"] = "addNotes"
    if (results.content)[1:-1] == b"true":
        return data
    return None


