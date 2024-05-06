import re
from pathlib import Path
from typing import List

from base.translate_meta import TranslationMeta
from models.languages import (
    SOURCE_FILE_2_DEEPL_MAP,
    DEEPL_2_SOURCE_FILE_MAP, SourceLangsCodes,
)
from settings.logger import logger


class TranslationServiceRPY(TranslationMeta):
    def __init__(self, source_lang_code: SourceLangsCodes = SourceLangsCodes.ENGLISH):
        super().__init__(source_lang_code)

    def translate_and_save_to_rpy(self, file_name: str):
        """Load RPY, translate and save to language-specific RPY files."""
        logger.info("Starting RPY translation process")
        input_file_path = self._SOURCE_DIR / file_name
        data = self._load_data(input_file_path)
        source_lang_deepl_format = SOURCE_FILE_2_DEEPL_MAP[self._source_lang_code]

        for target_lang_deepl_format, source_format_target_lang in DEEPL_2_SOURCE_FILE_MAP.items():
            if source_lang_deepl_format != target_lang_deepl_format:
                translated_data = [
                    self._translate_line(
                        line,
                        source_lang_deepl_format,
                        target_lang_deepl_format,
                    )
                    for line in data
                ]
                output_file_path = self._RESULT_DIR / f"{source_format_target_lang}__translate.rpy"
                self._save_data(translated_data, output_file_path)
                logger.info(f"Translation process completed for {source_format_target_lang}")

    @staticmethod
    def _load_data(file_path: Path) -> List[str]:
        """Load RPY file content into a list."""
        logger.debug(f"Loading RPY data from {file_path}")
        with file_path.open('r', encoding='utf-8') as file:
            lines = file.readlines()
        logger.debug("RPY data loaded successfully")
        return lines

    @staticmethod
    def _save_data(data: List[str], file_path: Path):
        """Save data to an RPY file."""
        logger.debug(f"Saving RPY data to {file_path}")
        with file_path.open('w', encoding='utf-8') as file:
            file.writelines(data)
        logger.debug("RPY data saved successfully")

    def _translate_line(self, line: str, source_lang: str, target_lang: str) -> str:
        """Check if line needs translation and translate if necessary."""
        match = re.match(r'^\s*(\w+\s")(.*)(")', line)
        if match:
            logger.debug(f"Found line to translate: {match.group(2)}")
            translated_text = self._translate_text(match.group(2), source_lang, target_lang)
            return f'\t{match.group(1)}{translated_text}{match.group(3)}\n'
        else:
            return line
