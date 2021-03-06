import requests
import json

ANKI_URL = "http://127.0.0.1:8765"
# ANKI_URL = "https://5602-79-183-2-134.eu.ngrok.io"


def update_by_id(id,fields):
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
    return json.loads(requests.post(ANKI_URL, data=json.dumps(data)).content)["result"]


def note_infos_by_regex(regex):
    a = find_notes(regex)
    if len(a) > 0 : 
        return note_info_by_ids(a)
    return []

def note_info_by_id(id):
    data = {
    "action":"notesInfo",
    "version":6,
    "params":{
        "notes":[id]
        }
    }
    return json.loads(requests.post(ANKI_URL, data=json.dumps(data)).content)["result"]


def note_info_by_ids(array_of_ids):
    infos = []
    for id in array_of_ids:
        data = {
        "action":"notesInfo",
        "version":6,
        "params":{
            "notes":[id]
            }
        }
        infos.append((id,json.loads(requests.post(ANKI_URL, data=json.dumps(data)).content)["result"]))
    return infos


def find_notes(regex):
    data = {
        "action":"findNotes",
        "version":6,
        "params":{
            "query":regex
        }
    }
    results = requests.post(ANKI_URL, data=json.dumps(data))
    return json.loads(results.content)["result"]

def add_note(deck_name, model_name, fields):
    data = {
        "version":6,
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
    print(fields)
    data["action"] = "canAddNotes"
    results = requests.post(ANKI_URL, data=json.dumps(data))
    data["action"] = "addNotes"
    print(results.content)
    if (json.loads(results.content))["result"][0] == True:
        print(json.loads(requests.post(ANKI_URL, data=json.dumps(data)).content)["result"])
        return data
    return None


