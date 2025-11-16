import os
import shutil
import webbrowser

from flask_cors import CORS
from flask import Flask, request
from sentence_generator import SentenceGenerator

app = Flask(__name__)
CORS(app, origins="*", methods=["GET", "POST"])


@app.get("/generatesentences")
def get_generate_sentences():
    sg = SentenceGenerator()
    return sg.generate_sentences()


if __name__ == "__main__":

    # create .env file if it doesn't exists
    if not os.path.exists('.env'):
        shutil.copyfile('.env_model', '.env')

    ui_path = os.path.join(".", "UI", "index.html")
    webbrowser.open(ui_path)

    app.run(host="127.0.0.1", port=5000)
    