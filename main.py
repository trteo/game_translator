from models.languages import (
    SourceLangsCodes,
    DEEPL_2_SOURCE_FILE_MAP,
)
from src.translatpr import TranslationService


if __name__ == '__main__':
    service = TranslationService(source_lang_code=SourceLangsCodes.RUSSIAN)
    service.translate_and_save_to_toml(languages=DEEPL_2_SOURCE_FILE_MAP)