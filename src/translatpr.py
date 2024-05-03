import requests
import toml
from typing import Dict
from settings.config import settings, BASE_DIR


SOURCE_DIR = BASE_DIR / 'data' / 'source'
RESULT_DIR = BASE_DIR / 'data' / 'result'


def translate_text(text: str, target_lang: str) -> str:
    url = "https://api-free.deepl.com/v2/translate"
    params = {
        "auth_key": settings.DEEPL_API_KEY,
        "text": text,
        "target_lang": target_lang
    }
    response = requests.post(url, data=params)
    if response.status_code == 200:
        return response.json()["translations"][0]["text"]
    else:
        return f"Translation failed with status code {response.status_code}"


def load_data_from_toml(file_path: str) -> Dict[str, str]:
    with open(file_path, "r", encoding="utf-8") as toml_file:
        return toml.load(toml_file)


def translate_and_save_to_toml(
    languages: Dict[str, str],
    input_file_path: str,
    output_file_path: str
) -> None:
    data_to_translate = load_data_from_toml(file_path=input_file_path)

    translations = {}
    for key, value in data_to_translate.items():
        translations[key] = {}
        for lang_code, lang_name in languages.items():
            translated_text = translate_text(text=value, target_lang=lang_code)
            translations[key][lang_code.lower()] = translated_text

    with open(output_file_path, "w", encoding="utf-8") as toml_file:
        toml.dump(translations, toml_file)


if __name__ == "__main__":
    languages: Dict[str, str] = {
        "EN-US": "eng",
        "UK": "ukr",
        "ES": "spa",
        "PT-BR": "pbr",
        "DE": "deu",
        "IT": "ita",
        "TR": "tur"
    }

    input_file_path = SOURCE_DIR / "cleanup.toml"
    output_file_path = RESULT_DIR / "translations.toml"

    translate_and_save_to_toml(
        languages=languages,
        input_file_path=input_file_path,
        output_file_path=output_file_path
    )
