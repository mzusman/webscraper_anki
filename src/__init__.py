from flask import Flask
from .app.anki import anki_bp 

app = Flask(__name__)
app.register_blueprint(anki_bp , url_prefix="/")

__name__ = "anki_webscrapper"