from pathlib import Path
import requests
import toml
from typing import Dict
from loguru import logger

from models.languages import (
    SOURCE_FILE_2_DEEPL_MAP,
    SourceLangsCodes, DEEPL_2_SOURCE_FILE_MAP,
)
from settings.config import settings, BASE_DIR


log_dir = BASE_DIR / "logs"

# Ensure the log directory exists.
log_dir.mkdir(parents=True, exist_ok=True)

# Configure loguru to log to a file within the logs directory.
logger.add(
    sink=log_dir / "translation_logs.log",  # Specifies the file path for the log file.
    rotation="10 MB",  # Specifies the maximum size of the log file before it rotates.
    retention="10 days",  # Optionally, specify how long to retain old log files.
    level="DEBUG"  # Specifies the minimum level of log messages to capture.
)

# Example of using the logger
logger.info("Logging setup is configured correctly.")


class TranslationService:
    _SOURCE_DIR = BASE_DIR / 'data' / 'source'
    _RESULT_DIR = BASE_DIR / 'data' / 'result'
    _LANGUAGES = DEEPL_2_SOURCE_FILE_MAP

    def __init__(self, source_lang_code: SourceLangsCodes = SourceLangsCodes.RUSSIAN):
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

    def translate_and_save_to_toml(self):
        """Load data, translate and save to another TOML file."""
        logger.info("Starting translation process")
        input_file_path = self._SOURCE_DIR / 'cleanup.toml'
        output_file_path = self._RESULT_DIR / 'translations.toml'

        data = self._load_data(input_file_path)
        translations = {}
        for key, values in data.items():
            translations[key] = {}
            for lang_code, lang_name in self._LANGUAGES.items():
                translations[key][lang_code.lower()] = self._translate_text(
                    text=values[self._source_lang_code.value],
                    source_file_lang=self._source_lang_code,
                    target_lang=lang_code,
                )

        self._save_data(data=translations, file_path=output_file_path)
        logger.info("Translation process completed")
