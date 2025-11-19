import os
import re
import json
import pandas as pd

from typing import List
from random import randrange
from langchain_google_genai import ChatGoogleGenerativeAI
from utils import (
    get_nb_sentences,
    get_vocab_path,
    get_target_language,
    get_selected_llm,
    get_GOOGLE_API_KEY,
)


class SentenceGenerator:
    def __init__(self):
        self.nb_sentences = get_nb_sentences()
        self.target_language = get_target_language()
        os.environ["GOOGLE_API_KEY"] = get_GOOGLE_API_KEY()
        self.model = ChatGoogleGenerativeAI(model=get_selected_llm())

    def generate_sentences(self) -> List[dict]:
        df_vocab = self.pick_random_terms_from_vocab()

        prompt = f"""
You are to generate a JSON with {self.nb_sentences} sentences in {self.target_language} and their english translation using only the following vocabulary words.

Vocabulary:
{df_vocab[['term', 'meanings', 'type']].to_string(index=False)}

Rules:
- You must ONLY use words from this list (but you don't have to use all of them).
- The sentences should make grammatical sense.
- Conjugate the verbs accordingly
- If needed, you can adapt the adjectives to the right gender/quantity
- If needed, you can add basic connectors like 'the', 'a', 'and', etc.

Generate {self.nb_sentences} sentences it the following format:
{{
    "sentences":[
        {{"sentence": "[GENERATED SENTENCE HERE]", "english": "[ENGLISH TRANSLATION HERE]"}},
    ],
    "type": "generated"
}}
        """

        # print(prompt)

        answer = self.model.invoke(prompt).content

        # print(answer)

        pattern = r'\{\s*"sentences"\s*:\s*\[.*?\]\s*,\s*"type"\s*:\s*"generated"\s*\}'
        match = re.search(pattern, answer, re.DOTALL)
        if match:
            json_str = match.group(0)
            data = json.loads(json_str)
            # print(data['sentences'])
            return data["sentences"]
        else:
            print("No JSON starting with 'sentences' found.")
            return []
        return []

    def pick_random_terms_from_vocab(self) -> pd.DataFrame:
        df = pd.read_csv(get_vocab_path())

        max_nb_noun = min(self.nb_sentences * 2, len(df[df["type"] == "noun"]))
        max_nb_verb = min(
            self.nb_sentences + self.nb_sentences // 2, len(df[df["type"] == "verb"])
        )
        max_nb_adj = min(self.nb_sentences // 2, len(df[df["type"] == "adjective"]))
        max_nb_adv = min(self.nb_sentences // 3, len(df[df["type"] == "adverb"]))

        random_nouns = df[df["type"] == "noun"].sample(
            n=randrange(max_nb_noun // 2, max_nb_noun)
        )
        random_verbs = df[df["type"] == "verb"].sample(
            n=randrange(max_nb_verb // 2, max_nb_verb)
        )
        random_adjs = df[df["type"] == "adjective"].sample(
            n=randrange(max_nb_adj // 2, max_nb_adj)
        )
        random_advs = df[df["type"] == "adverb"].sample(
            n=randrange(max_nb_adv // 2, max_nb_adv)
        )

        df_vocab = pd.concat([random_nouns, random_verbs, random_adjs, random_advs])

        return df_vocab
