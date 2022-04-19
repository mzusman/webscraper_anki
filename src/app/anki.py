from flask import Blueprint
from ..service import utils
import json
anki_bp = Blueprint('anki',__name__)

@anki_bp.route("/")
def hw():
    return "Hello"

@anki_bp.route("/getIdby/<regex>")
def id(regex):
    a = (utils.find_notes(regex))
    return json.dumps(a)

@anki_bp.route("/getInfoBy/<regex>")
def info(regex):
    a = (utils.note_infos_by_regex(regex))
    return json.dumps(a,ensure_ascii=False)

@anki_bp.route("/getInfoBy/<regex>")
def info(regex):
    a = (utils.note_infos_by_regex(regex))
    return json.dumps(a,ensure_ascii=False)