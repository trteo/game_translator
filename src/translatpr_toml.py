from pathlib import Path
import toml
from typing import Dict
from loguru import logger
from models.languages import (
    SOURCE_FILE_2_DEEPL_MAP,
    SourceLangsCodes, DEEPL_2_SOURCE_FILE_MAP,
)
from base.translate_meta import TranslationMeta


class TranslationServiceTOML(TranslationMeta):
    def __init__(self, source_lang_code: SourceLangsCodes = SourceLangsCodes.RUSSIAN):
        super().__init__(source_lang_code)

    def translate_and_save_to_toml(self):
        """Load data, translate and save to another TOML file."""
        logger.info("Starting translation process")
        input_file_path = self._SOURCE_DIR / 'cleanup.toml'
        output_file_path = self._RESULT_DIR / 'translations.toml'

        data = self._load_data(input_file_path)
        translations = {}
        for key, values in data.items():
            translations[key] = {}
            for target_lang, lang_name in DEEPL_2_SOURCE_FILE_MAP.items():
                source_lang = SOURCE_FILE_2_DEEPL_MAP[self._source_lang_code]
                if source_lang != target_lang:
                    translations[key][target_lang.lower()] = self._translate_text(
                        text=values[self._source_lang_code.value],
                        source_lang=source_lang,
                        target_lang=target_lang,
                    )

        self._save_data(data=translations, file_path=output_file_path)
        logger.info("Translation process completed")

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
