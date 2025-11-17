import os
import shutil
import webbrowser

from flask_cors import CORS
from flask import Flask, request
from sentence_generator import SentenceGenerator
from sentence_evaluator import calculate_score, get_diff_between_sentences, remove_punctuation

app = Flask(__name__)
CORS(app, origins="*", methods=["GET", "POST"])


@app.get("/generatesentences")
def get_generate_sentences():
    sg = SentenceGenerator()
    return sg.generate_sentences()


@app.post("/evaluatesentences")
def post_evaluate_sentences():
    data = request.get_json()
    sentences = data["sentences"]

    for s in sentences:
        clean_text = remove_punctuation(s["answer"]).lower()
        clean_reference = remove_punctuation(s["sentence"]).lower()
        s["diff"] = get_diff_between_sentences(clean_text, clean_reference)
        s["score"] = f"{calculate_score(clean_text, clean_reference)}%"

    return sentences


if __name__ == "__main__":

    # create .env file if it doesn't exists
    if not os.path.exists('.env'):
        shutil.copyfile('.env_model', '.env')

    # ui_path = os.path.join(".", "UI", "index.html")
    # webbrowser.open(ui_path)

    app.run(host="127.0.0.1", port=5000)
    