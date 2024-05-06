from models.languages import SourceLangsCodes
from src.translatpr_rpy import TranslationServiceRPY
from src.translatpr_toml import TranslationServiceTOML

if __name__ == '__main__':
    # Instantiate and use the TOML translation service
    toml_service = TranslationServiceTOML(source_lang_code=SourceLangsCodes.ENGLISH)
    toml_service.translate_and_save(
        file_name='cleanup.toml', output_name='translations.toml'
    )

    # Instantiate and use the RPY translation service
    rpy_service = TranslationServiceRPY(source_lang_code=SourceLangsCodes.ENGLISH)
    rpy_service.translate_and_save(file_name='test.rpy', output_name='translations.rpy')
