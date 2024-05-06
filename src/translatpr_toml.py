from pathlib import Path
import toml
from typing import Dict, Any
from settings.logger import logger
from models.languages import (
    SOURCE_FILE_2_DEEPL_MAP,
    SourceLangsCodes,
    DEEPL_2_SOURCE_FILE_MAP,
)
from base.translate_meta import TranslationMeta

class TranslationServiceTOML(TranslationMeta):
    def __init__(self, source_lang_code: SourceLangsCodes = SourceLangsCodes.RUSSIAN):
        super().__init__(source_lang_code=source_lang_code)

    def process_translations(self, data: Dict[str, Dict[str, str]]) -> Dict[str, Dict[str, str]]:
        """Process the translations from the source language to multiple target languages."""
        translations: Dict[str, Dict[str, str]] = {}
        source_lang_deepl_format: str = SOURCE_FILE_2_DEEPL_MAP[self._source_lang_code]

        for block_header, existing_translations in data.items():
            translations[block_header] = {}
            text_to_translate: str = existing_translations[self._source_lang_code.value]
            for target_lang_deepl_format, source_format_target_lang in DEEPL_2_SOURCE_FILE_MAP.items():
                if source_lang_deepl_format != target_lang_deepl_format:
                    translated_text: str = self._translate_text(
                        text=text_to_translate,
                        source_lang=source_lang_deepl_format,
                        target_lang=target_lang_deepl_format
                    )
                    translations[block_header][source_format_target_lang.lower()] = translated_text

        return translations

    @staticmethod
    def _load_data(file_path: Path) -> Dict[str, Any]:
        """Load data from a TOML file."""
        logger.debug(f'Loading data from {file_path}')
        with file_path.open('r', encoding='utf-8') as file:
            data: Dict[str, Any] = toml.load(file)
        logger.debug('Data loaded successfully')
        return data

    @staticmethod
    def _save_data(data: Dict[str, Any], file_path: Path) -> None:
        """Save data to a TOML file."""
        logger.debug(f'Saving data to {file_path}')
        with file_path.open('w', encoding='utf-8') as toml_file:
            toml.dump(data, toml_file)
        logger.debug('Data saved successfully')

