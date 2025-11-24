import os
import deepl

from utils import use_deepl_translation

class Translator:
    def __init__(self):
        if use_deepl_translation():
            self.deepl_client = deepl.DeepLClient(os.getenv("DEEPL_API_KEY"))


    def get_deepl_tranlation(self, text: str, target_language_code: str) -> str:
        try:
            result = self.deepl_client.translate_text(text, source_lang="EN", target_lang=target_language_code, extra_body_parameters={"enable_beta_languages":True})
            return result.text
        except Exception as e:
            print("DeepL Translator:", e)
            return ""