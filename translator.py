import os
import deepl

from typing import Optional
from utils import use_deepl_translation


class Translator:
    def __init__(self):
        if use_deepl_translation():
            self.deepl_client = deepl.DeepLClient(os.getenv("DEEPL_API_KEY"))
            glossary_languages = self.deepl_client.get_glossary_languages()
            self.available_glossary = set()
            for language_pair in glossary_languages:
                if language_pair.source_lang.upper() == "EN":
                    self.available_glossary.add(language_pair.target_lang.upper())

    def get_deepl_tranlation(
        self, text: str, target_language_code: str, glossary_id: Optional[str] = None
    ) -> str:
        try:
            result = self.deepl_client.translate_text(
                text,
                source_lang="EN",
                target_lang=target_language_code,
                extra_body_parameters={"enable_beta_languages": True},
                glossary=glossary_id,
            )
            return result.text
        except Exception as e:
            print("DeepL Translator:", e)
            return ""

    def deepl_create_request_glossary(
        self, vocab: dict, target_language_code: str, request_id: str
    ) -> Optional[str]:
        if target_language_code in self.available_glossary:
            dictionaries = [
                deepl.api_data.MultilingualGlossaryDictionaryEntries(
                    "EN", target_language_code, vocab
                )
            ]
            my_glossary = self.deepl_client.create_multilingual_glossary(
                request_id, dictionaries
            )
            return my_glossary.glossary_id
        return None

    def deepl_delete_request_glossary(self, glossary_id: str) -> None:
        self.deepl_client.delete_multilingual_glossary(glossary_id)
