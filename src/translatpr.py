from pathlib import Path
import requests
import toml
from typing import Dict
from loguru import logger

from models.languages import (
    SOURCE_FILE_2_DEEPL_MAP,
    SourceLangsCodes,
    DEEPL_2_SOURCE_FILE_MAP,
)
from settings.config import settings, BASE_DIR

logger.add(BASE_DIR / "logs/translation_logs.log", rotation="10 MB")


class TranslationService:
    _source_dir = BASE_DIR / 'data' / 'source'
    _result_dir = BASE_DIR / 'data' / 'result'

    def __init__(self, source_lang_code: SourceLangsCodes):
        self._source_lang_code = source_lang_code
        logger.info(f"Translation service initialized for source language: {self._source_lang_code}")

    @staticmethod
    def _translate_text(text: str, source_file_lang: SourceLangsCodes, target_lang: str) -> str:
        """Translate text from source language to target language using DeepL API."""
        logger.debug(f"Translating text from {source_file_lang} to {target_lang}")
        url = 'https://api-free.deepl.com/v2/translate'
        params = {
            'auth_key': settings.DEEPL_API_KEY,
            'text': text,
            'source_lang': SOURCE_FILE_2_DEEPL_MAP.get(source_file_lang),
            'target_lang': target_lang,
        }
        response = requests.post(url, params=params)
        if response.status_code == 200:
            translated_text = response.json()['translations'][0]['text']
            logger.debug(f"Translation successful: {translated_text}")
            return translated_text
        else:
            logger.error(f"Translation failed with status code {response.status_code}")
            return f"Translation failed with status code {response.status_code}"

    @staticmethod
    def _load_data(file_path: Path) -> Dict:
        """Load data from a TOML file."""
        logger.debug(f"Loading data from {file_path}")
        with file_path.open('r', encoding='utf-8') as file:
            data = toml.load(file)
        logger.debug("Data loaded successfully")
        return data

    @staticmethod
    def _save_data(data: Dict, file_path: Path):
        """Save data to a TOML file."""
        logger.debug(f"Saving data to {file_path}")
        with file_path.open('w', encoding='utf-8') as toml_file:
            toml.dump(data, toml_file)
        logger.debug("Data saved successfully")

    def translate_and_save_to_toml(self, languages: Dict[str, str]):
        """Load data, translate and save to another TOML file."""
        logger.info("Starting translation process")
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

        self._save_data(data=translations, file_path=output_file_path)
        logger.info("Translation process completed")


if __name__ == '__main__':
    source_lang_code = SourceLangsCodes.RUSSIAN
    service = TranslationService(source_lang_code=source_lang_code)
    service.translate_and_save_to_toml(languages=DEEPL_2_SOURCE_FILE_MAP)
