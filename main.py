from models.languages import (
    SourceLangsCodes,
    DEEPL_2_SOURCE_FILE_MAP,
)
from src.translatpr_rpy import TranslationServiceRPY
from src.translatpr_toml import TranslationServiceTOML


# if __name__ == '__main__':
#     service = TranslationServiceTOML(source_lang_code=SourceLangsCodes.ENGLISH)
#     service.translate_and_save_to_toml()

#
if __name__ == '__main__':
    service = TranslationServiceRPY(source_lang_code='EN')
    service.translate_and_save_to_rpy(languages=DEEPL_2_SOURCE_FILE_MAP, file_name='test.rpy')