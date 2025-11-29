import os
import shutil
import webbrowser

from flask_cors import CORS
from flask import Flask, request
from translator import Translator
from database_manager import create_database, get_request_vocab, get_sentence
from sentence_generator import SentenceGenerator
from sentence_evaluator import (
    calculate_score,
    get_diff_between_sentences,
    remove_punctuation,
)
from utils import (
    get_nb_sentences,
    get_vocab_path,
    get_vocab_folder,
    get_all_vocabs,
    get_selected_llm,
    get_all_llms,
    set_nb_sentences,
    set_use_deepl_translation,
    set_vocab,
    set_selected_llm,
    use_deepl_translation,
)

app = Flask(__name__)
CORS(app, origins="*", methods=["GET", "POST"])


@app.get("/getparameters")
def get_parameters():
    return {
        "nb_sentences": get_nb_sentences(),
        "selected_vocab": get_vocab_path(),
        "vocab_folder": get_vocab_folder(),
        "vocab_list": get_all_vocabs(),
        "llms": get_all_llms(),
        "selected_llm": get_selected_llm(),
        "deepl_enabled": os.getenv("DEEPL_API_KEY").strip() != "",
        "use_deepl": use_deepl_translation(),
    }


@app.post("/updateparameters")
def post_update_parameters():
    data = request.get_json()
    errors = []
    if not set_nb_sentences(int(data["nb_sentences"])):
        errors.append("Error when updating number of sentences!")
    if not set_vocab(data["selected_vocab"]):
        errors.append("Error when updating the selected vocabulary!")
    if not set_selected_llm(data["selected_llm"]):
        errors.append("Error when updating selected LLM!")
    if not set_use_deepl_translation(data["use_deepl"]):
        errors.append("Error when updating DeepL usage!")

    return {"status": "ok"} if len(errors) == 0 else {"status": "nok", "errors": errors}


@app.get("/generatesentences")
def get_generate_sentences():
    sg = SentenceGenerator()
    return sg.generate_sentences()


@app.post("/evaluatesentences")
def post_evaluate_sentences():
    data = request.get_json()
    sentences = data["sentences"]

    if use_deepl_translation():
        t = Translator()
        vocab = get_request_vocab(data["request_id"])
        glossary_id = t.deepl_create_request_glossary(
            vocab=vocab,
            target_language_code=data["target_lang"],
            request_id=data["request_id"],
        )

    for s in sentences:
        sentence_data = get_sentence(s["sentence_id"])

        clean_text = remove_punctuation(s["answer"]).lower()
        clean_reference = remove_punctuation(sentence_data["translation"]).lower()
        s["sentence"] = sentence_data["translation"]
        score = calculate_score(clean_text, clean_reference)

        if use_deepl_translation() and score < 100:
            trans_reference = t.get_deepl_tranlation(
                text=sentence_data["english"],
                target_language_code=sentence_data["language_code"],
                glossary_id=glossary_id,
            )
            print(
                f"{sentence_data["english"]}({sentence_data["translation"]}) DeepL tranlate: {trans_reference}"
            )
            trans_score = calculate_score(clean_text, remove_punctuation(trans_reference).lower())
            if trans_score > score:
                score = trans_score
                clean_reference = remove_punctuation(trans_reference).lower()
                s["sentence"] = trans_reference

        s["diff"] = get_diff_between_sentences(clean_text, clean_reference)
        s["score"] = f"{score}%"

    if glossary_id:
        t.deepl_delete_request_glossary(glossary_id)

    return sentences


if __name__ == "__main__":

    # create .env file if it doesn't exists
    if not os.path.exists(".env"):
        shutil.copyfile(".env_model", ".env")

    create_database()

    ui_path = os.path.join(".", "UI", "index.html")
    webbrowser.open(ui_path)

    app.run(host="127.0.0.1", port=5000)
