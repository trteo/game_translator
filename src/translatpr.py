from pathlib import Path
import requests
import toml
from typing import Dict

from models.languages import (
    SOURCE_FILE_2_DEEPL_MAP,
    SourceLangsCodes,
    DEEPL_2_SOURCE_FILE_MAP,
)
from settings.config import settings, BASE_DIR


class TranslationService:
    _source_dir = BASE_DIR / 'data' / 'source'
    _result_dir = BASE_DIR / 'data' / 'result'

    def __init__(self, source_lang_code: SourceLangsCodes):
        self._source_lang_code = source_lang_code

    @classmethod
    def _translate_text(cls, text: str, source_file_lang: SourceLangsCodes, target_lang: str) -> str:
        """Translate text from source language to target language using DeepL API."""
        url = 'https://api-free.deepl.com/v2/translate'
        params = {
            'auth_key': settings.DEEPL_API_KEY,
            'text': text,
            'source_lang': SOURCE_FILE_2_DEEPL_MAP.get(source_file_lang),
            'target_lang': target_lang,
        }
        response = requests.post(url, data=params)
        if response.status_code == 200:
            return response.json()['translations'][0]['text']
        else:
            return f'Translation failed with status code {response.status_code}'

    def _load_data(self, file_path: Path) -> Dict:
        """Load data from a TOML file."""
        with file_path.open('r', encoding='utf-8') as file:
            return toml.load(file)

    def _save_data(self, data: Dict, file_path: Path):
        """Save data to a TOML file."""
        with file_path.open('w', encoding='utf-8') as toml_file:
            toml.dump(data, toml_file)

    def translate_and_save_to_toml(self, languages: Dict[str, str]):
        """Load data, translate and save to another TOML file."""
        input_file_path = self._source_dir / 'cleanup.toml'
        output_file_path = self._result_dir / 'translations.toml'

        data = self._load_data(input_file_path)
        translations = {}
        for key, values in data.items():
            translations[key] = {}
            for lang_code, lang_name in languages.items():
                translations[key][lang_code.lower()] = self._translate_text(
                    text=values[self._source_lang_code.value],
                    source_file_lang=self._source_lang_code,
                    target_lang=lang_code,
                )

        self._save_data(translations, output_file_path)


if __name__ == '__main__':
    service = TranslationService(SourceLangsCodes.RUSSIAN)
    service.translate_and_save_to_toml(DEEPL_2_SOURCE_FILE_MAP)
