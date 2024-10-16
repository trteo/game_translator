from models.languages import SourceLangsCodes
from src.translators.deepl.translatpr_rpy import DeeplTranslationServiceRPY
from src.translators.deepl.translatpr_toml import DeeplTranslationServiceTOML

if __name__ == '__main__':
    # Instantiate and use the TOML translation service
    toml_service = DeeplTranslationServiceTOML(source_lang_code=SourceLangsCodes.ENGLISH)
    toml_service.translate_and_save(
        file_name='cleanup.toml', output_name='translations.toml'
    )

    # Instantiate and use the RPY translation service
    rpy_service = DeeplTranslationServiceRPY(source_lang_code=SourceLangsCodes.ENGLISH)
    rpy_service.translate_and_save(file_name='test.rpy', output_name='translations.rpy')
