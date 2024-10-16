from abc import abstractmethod, ABC
from pathlib import Path
import requests
from typing import Any, Dict, TypeVar

from models.languages import SourceLangsCodes
from settings.logger import logger
from settings.config import settings, BASE_DIR

# Define a generic variable for data type that will be implemented by subclasses
T = TypeVar('T')


class DeeplTranslationABC(ABC):
    _SOURCE_DIR: Path = BASE_DIR / 'data' / 'source'
    _RESULT_DIR: Path = BASE_DIR / 'data' / 'result'

    def __init__(self, source_lang_code: SourceLangsCodes):
        self._source_lang_code = source_lang_code
        logger.info(
            f'Translation service initialized for source language: {self._source_lang_code}'
        )

    def translate_and_save(self, file_name: str, output_name: str) -> None:
        """Orchestrate the process of loading data, processing translations, and saving them."""
        logger.info('Starting translation process')
        input_file_path: Path = self._SOURCE_DIR / file_name
        output_file_path: Path = self._RESULT_DIR / output_name

        data: T = self._load_data(file_path=input_file_path)
        translations: T = self.process_translations(data=data)

        self._save_data(data=translations, file_path=output_file_path)
        logger.info('Translation process completed')

    def process_translations(self, data: T) -> T:
        """
        Process translation according to the specific rules of the subclass.
        Should be implemented by each subclass.
        """

    @staticmethod
    def _translate_text(text: str, source_lang: str, target_lang: str) -> str:
        """Translate text from source language to target language using DeepL API."""
        logger.debug(f'Translating text from {source_lang} to {target_lang}')
        url: str = 'https://api-free.deepl.com/v2/translate'
        params: Dict[str, str] = {
            'auth_key': settings.DEEPL_API_KEY,
            'text': text,
            'source_lang': source_lang,
            'target_lang': target_lang,
        }
        response = requests.post(url, params=params)
        if response.status_code == 200:
            translated_text: str = response.json()['translations'][0]['text']
            logger.debug(f'Translation successful: {translated_text}')
            return translated_text
        else:
            logger.error(
                f'Translation failed with status code {response.status_code}: {response.text}'
            )
            return f'Translation failed with status code {response.status_code}'

    @staticmethod
    @abstractmethod
    def _load_data(file_path: Path) -> T:
        """Generic data loading method, must be implemented by subclasses to handle specific data formats."""

    @staticmethod
    @abstractmethod
    def _save_data(data: T, file_path: Path) -> None:
        """Generic data saving method, must be implemented by subclasses to handle specific data formats."""
