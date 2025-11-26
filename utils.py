import os
import csv
import json

from typing import List, Tuple
from dotenv import load_dotenv

load_dotenv()


def get_GOOGLE_API_KEY() -> str:
    return os.getenv("GOOGLE_API_KEY")


def get_nb_sentences() -> int:
    with open("config.json", "r") as file:
        data = json.load(file)
        return data["nb_sentences"]
    return 0


def set_nb_sentences(nb: int) -> bool:
    with open("config.json", "r") as file:
        data = json.load(file)
    data["nb_sentences"] = nb
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
        return True
    return False


def get_vocab_folder() -> str:
    with open("config.json", "r") as file:
        data = json.load(file)
        assert os.path.exists(
            data["vocab_folder"]
        ), f"{data['vocab_folder']} doesn't exists!"
        return data["vocab_folder"]
    return ""


def get_all_vocabs() -> List[Tuple[str, str]]:
    res = []
    with open("config.json", "r") as file:
        config_data = json.load(file)
        vocab_folder = config_data["vocab_folder"]
        assert os.path.exists(vocab_folder), f"{vocab_folder} doesn't exists!"
        for dirpath, dirnames, filenames in os.walk(vocab_folder):
            if dirpath == vocab_folder:
                continue  # root folder
            if "vocab_info.json" not in filenames:
                continue  # no vocab_info.json in folder

            vocab_info_path = os.path.join(dirpath, "vocab_info.json")
            try:
                with open(vocab_info_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if "target_language" in data and "vocab_file" in data:
                        vocab_file_path = os.path.join(dirpath, data["vocab_file"])
                        if not os.path.exists(vocab_file_path):
                            continue  # vocab file doesn't exists

                        try:
                            with open(
                                vocab_file_path, newline="", encoding="utf-8"
                            ) as f:
                                reader = csv.DictReader(f)
                                headers = set(reader.fieldnames or [])
                        except Exception:
                            continue  # skip unreadable or invalid CSV

                        if not {"term", "meanings", "type"}.issubset(headers):
                            continue  # vocab csv doesn't contains the right headers

                        res.append((data["target_language"], vocab_file_path))
                    else:
                        continue  # vocab_info.json doesn't have target_language or vocab_file
            except (json.JSONDecodeError, OSError):
                continue  # JSON no properly formatted
    return res


def get_target_language() -> str:
    with open("config.json", "r") as file:
        data = json.load(file)
        return data["selected_target_language"]
    return ""


def get_target_language_code() -> str:
    with open("config.json", "r") as file:
        data = json.load(file)
        vocab_folder = os.path.dirname(data["selected_vocab_file"])
        vocab_info = os.path.join(vocab_folder, "vocab_info.json")
        if os.path.exists(vocab_info):
            with open(vocab_info) as v_i:
                v_i = json.load(v_i)
                if "target_language_code" in v_i:
                    return v_i["target_language_code"]
    return ""


def set_vocab(vocab_path: str) -> bool:
    if not os.path.exists(vocab_path):
        return False

    folder = os.path.dirname(vocab_path)
    if not os.path.exists(os.path.join(folder, "vocab_info.json")):
        return False

    with open("config.json", "r") as file:
        data = json.load(file)
    with open(os.path.join(folder, "vocab_info.json"), "r") as f:
        vocab_info = json.load(f)

    data["selected_vocab_file"] = os.path.join(folder, vocab_info["vocab_file"])
    data["selected_target_language"] = vocab_info["target_language"]

    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
        return True
    return False


def get_vocab_path() -> str:
    with open("config.json", "r") as file:
        data = json.load(file)
        assert os.path.exists(
            data["selected_vocab_file"]
        ), f"{data['selected_vocab_file']} doesn't exists!"
        return data["selected_vocab_file"]
    return None


def get_selected_llm() -> str:
    with open("config.json", "r") as file:
        data = json.load(file)
        return data["selected_llm"]
    return ""


def set_selected_llm(llm: str) -> bool:
    with open("config.json", "r") as file:
        data = json.load(file)
    data["selected_llm"] = llm
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
        return True
    return False


def get_all_llms() -> List[str]:
    with open("config.json", "r") as file:
        data = json.load(file)
        return data["available_llms"]
    return ""


def use_deepl_translation() -> bool:
    with open("config.json", "r") as file:
        data = json.load(file)
        return data["use_deepl_translation"]
    return False


def get_all_languages() -> List[Tuple[str, str]]:
    languages = []
    vocab_folder = get_vocab_folder()
    for dirpath, dirnames, filenames in os.walk(vocab_folder):
        if dirpath == vocab_folder:
            continue
        if "vocab_info.json" not in filenames:
            continue

        vocab_info_path = os.path.join(dirpath, "vocab_info.json")
        if os.path.exists(vocab_info_path):
            with open(vocab_info_path, "r") as vocab_info:
                vocab_info_data = json.load(vocab_info)
                if (
                    "target_language_code" in vocab_info_data
                    and "target_language" in vocab_info_data
                ):
                    languages.append(
                        (
                            vocab_info_data["target_language_code"],
                            vocab_info_data["target_language"],
                        )
                    )
    return languages
