import re
from pathlib import Path
from typing import List

from base.translate_meta import TranslationMeta
from models.languages import (
    SOURCE_FILE_2_DEEPL_MAP,
    DEEPL_2_SOURCE_FILE_MAP,
    SourceLangsCodes,
)
from settings.logger import logger


class TranslationServiceRPY(TranslationMeta):
    def __init__(self, source_lang_code: SourceLangsCodes = SourceLangsCodes.ENGLISH):
        super().__init__(source_lang_code)

    def process_translations(self, data):
        source_lang_deepl_format = SOURCE_FILE_2_DEEPL_MAP[self._source_lang_code]
        translations = []
        for line in data:
            for target_lang_deepl_format, source_format_target_lang in DEEPL_2_SOURCE_FILE_MAP.items():
                if source_lang_deepl_format != target_lang_deepl_format:
                    translated_line = self._translate_line(line, source_lang_deepl_format, target_lang_deepl_format)
                    translations.append(translated_line)
        return translations

    @staticmethod
    def _load_data(file_path: Path) -> List[str]:
        """Load RPY file content into a list."""
        logger.debug(f'Loading RPY data from {file_path}')
        with file_path.open('r', encoding='utf-8') as file:
            lines = file.readlines()
        logger.debug('RPY data loaded successfully')
        return lines

    @staticmethod
    def _save_data(data: List[str], file_path: Path):
        """Save data to an RPY file."""
        logger.debug(f'Saving RPY data to {file_path}')
        with file_path.open('w', encoding='utf-8') as file:
            file.writelines(data)
        logger.debug('RPY data saved successfully')

    def _translate_line(self, line: str, source_lang: str, target_lang: str) -> str:
        """Check if line needs translation and translate if necessary."""
        match = re.match(r'^\s*(\w+\s")(.*)(")', line)
        if match:
            logger.debug(f'Found line to translate: {match.group(2)}')
            translated_text = self._translate_text(
                match.group(2), source_lang, target_lang
            )
            return f'\t{match.group(1)}{translated_text}{match.group(3)}\n'
        else:
            return line
