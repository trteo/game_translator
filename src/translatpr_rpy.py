from pathlib import Path
import re
import requests
from typing import Dict, List
from loguru import logger

from settings.config import settings, BASE_DIR

log_dir = BASE_DIR / "logs"
log_dir.mkdir(parents=True, exist_ok=True)
logger.add(sink=log_dir / "translation_logs.log", rotation="10 MB", retention="10 days", level="DEBUG")


class RPYTranslationService:
    _source_dir = BASE_DIR / 'data' / 'source'
    _result_dir = BASE_DIR / 'data' / 'result'

    def __init__(self, source_lang_code: str):
        self._source_lang_code = source_lang_code
        logger.info(f"RPY Translation service initialized for source language: {self._source_lang_code}")

    @staticmethod
    def _translate_text(text: str, target_lang: str) -> str:
        """Translate text from source language to target language using DeepL API."""
        logger.debug(f"Translating text to {target_lang}")
        url = 'https://api-free.deepl.com/v2/translate'
        params = {
            'auth_key': settings.DEEPL_API_KEY,
            'text': text,
            'source_lang': 'EN',  # Assuming source language is always English
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

    def translate_and_save_to_rpy(self, languages: Dict[str, str], file_name: str):
        """Load RPY, translate and save to language-specific RPY files."""
        input_file_path = self._source_dir / file_name
        data = self._load_rpy_data(input_file_path)

        for lang_code in languages.keys():
            translated_data = [self._translate_line(line, lang_code) for line in data]
            output_file_path = self._result_dir / f"{lang_code}__translate.rpy"
            self._save_data(translated_data, output_file_path)
            logger.info(f"Translation process completed for {lang_code}")

    @staticmethod
    def _load_rpy_data(file_path: Path) -> List[str]:
        """Load RPY file content into a list."""
        logger.debug(f"Loading data from {file_path}")
        with file_path.open('r', encoding='utf-8') as file:
            lines = file.readlines()
        logger.debug("Data loaded successfully")
        return lines

    @staticmethod
    def _save_data(data: List[str], file_path: Path):
        """Save data to an RPY file."""
        logger.debug(f"Saving data to {file_path}")
        with file_path.open('w', encoding='utf-8') as file:
            file.writelines(data)
        logger.debug("Data saved successfully")

    def _translate_line(self, line: str, lang_code: str) -> str:
        """Check if line needs translation and translate if necessary."""
        match = re.match(r'(.*m ")(.*)(")', line)
        if match:
            logger.debug(f"Found line to translate: {match.group(2)}")
            return f'{match.group(1)}{self._translate_text(match.group(2), lang_code)}{match.group(3)}\n'
        else:
            return line


if __name__ == '__main__':
    languages = {'ES': 'ES', 'DE': 'DE', 'FR': 'FR'}  # Define the target languages
    service = RPYTranslationService(source_lang_code='EN')
    service.translate_and_save_to_rpy(languages=languages, file_name='test.rpy')
