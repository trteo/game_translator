from models.languages import (
    SourceLangsCodes,
    DEEPL_2_SOURCE_FILE_MAP,
)
from src.translatpr_rpy import RPYTranslationService
from src.translatpr_toml import TranslationService


if __name__ == '__main__':
    service = TranslationService(source_lang_code=SourceLangsCodes.RUSSIAN)
    service.translate_and_save_to_toml(languages=DEEPL_2_SOURCE_FILE_MAP)


if __name__ == '__main__':
    service = RPYTranslationService(source_lang_code='EN')
    service.translate_and_save_to_rpy(languages=DEEPL_2_SOURCE_FILE_MAP, file_name='test.rpy')