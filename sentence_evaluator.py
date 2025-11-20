import string
import Levenshtein

from difflib import Differ
from typing import List, Tuple

def remove_punctuation(txt: str) -> str:
    return txt.translate(str.maketrans('', '', string.punctuation))


def get_diff_between_sentences(text: str, reference: str) -> List[Tuple[str, str]]:
    d = Differ()
    diff = [
        (token[2:], token[0])
        for token in d.compare(text.split(), reference.split())
        if token[0] in {'+', '-', ' '}
    ]

    return diff


def calculate_score(text: str, reference: str) -> float:
    distance = Levenshtein.distance(text, reference)
    max_len = max(len(text), len(reference))

    if max_len == 0:
        return 100.0  
    similarity = 1 - (distance / max_len)
    return round(similarity * 100, 2)