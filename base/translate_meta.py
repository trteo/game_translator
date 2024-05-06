from pathlib import Path
import requests
from typing import Dict
from loguru import logger
from settings.config import settings, BASE_DIR


# Setup common logging for all translation services
log_dir = BASE_DIR / "logs"
log_dir.mkdir(parents=True, exist_ok=True)
logger.add(
    sink=log_dir / "translation_logs.log",
    rotation="10 MB",
    retention="10 days",
    level="DEBUG"
)


class TranslationMeta:
    _SOURCE_DIR = BASE_DIR / 'data' / 'source'
    _RESULT_DIR = BASE_DIR / 'data' / 'result'

    def __init__(self, source_lang_code):
        self._source_lang_code = source_lang_code
        logger.info(f"Translation service initialized for source language: {self._source_lang_code}")

    @staticmethod
    def _translate_text(text: str, source_lang: str, target_lang: str) -> str:
        """Translate text from source language to target language using DeepL API."""
        logger.debug(f"Translating text from {source_lang} to {target_lang}")
        url = 'https://api-free.deepl.com/v2/translate'
        params = {
            'auth_key': settings.DEEPL_API_KEY,
            'text': text,
            'source_lang': source_lang,
            'target_lang': target_lang
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
    def _load_data(file_path: Path):
        """Generic data loading method, implemented by subclasses."""
        raise NotImplementedError("This method should be overridden by subclasses.")

    @staticmethod
    def _save_data(data, file_path: Path):
        """Generic data saving method, implemented by subclasses."""
        raise NotImplementedError("This method should be overridden by subclasses.")
