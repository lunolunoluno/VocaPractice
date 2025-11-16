import os 
import json

from dotenv import load_dotenv
load_dotenv()

def get_GOOGLE_API_KEY() -> str:
    return os.getenv('GOOGLE_API_KEY') 


def get_nb_sentences() -> int:
    with open('config.json', 'r') as file:
        data = json.load(file)
        return data['nb_sentences']
    return 0


def get_target_language() -> str:
    with open('config.json', 'r') as file:
        data = json.load(file)
        return data['target_language']
    return ''


def get_vocab_path() -> str:
    with open('config.json', 'r') as file:
        data = json.load(file)
        assert os.path.exists(data['vocab_file']), f"{data['vocab_file']} doesn't exists!"
        return data['vocab_file']
    return None


