from enum import Enum
from pathlib import Path

import requests
import toml
from typing import Dict
from settings.config import settings, BASE_DIR


SOURCE_DIR = BASE_DIR / 'data' / 'source'
RESULT_DIR = BASE_DIR / 'data' / 'result'


SOURCE_FILE_2_DEEPL_MAP = {
    'eng': 'EN',
    'rus': 'RU',
}


class SourceLangs(Enum):
    EN = 'EN'
    RU = 'RU'


def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    """Translate text from source language to target language using DeepL API."""
    url = "https://api-free.deepl.com/v2/translate"
    params = {
        "auth_key": settings.DEEPL_API_KEY,
        "text": text,
        "source_lang": 'EN',
        "target_lang": target_lang
    }
    response = requests.post(url, data=params)
    if response.status_code == 200:
        return response.json()["translations"][0]["text"]
    else:
        return f"Translation failed with status code {response.status_code}"


def translate_and_save_to_toml(
        languages: Dict[str, str],
        input_file_path: Path,
        output_file_path: Path,
        source_lang_code: str
) -> None:
    """Load data from TOML, translate and save to another TOML file."""
    # Load original data
    with input_file_path.open("r", encoding="utf-8") as file:
        data = toml.load(file)

    translations = {}
    for key, values in data.items():
        translations[key] = {}
        for lang_code, lang_name in languages.items():
            # Translate each term using the source language provided
            translations[key][lang_code.lower()] = translate_text(values[source_lang_code], source_lang_code, lang_code)

    # Save translations to new TOML file
    with output_file_path.open("w", encoding="utf-8") as toml_file:
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

    # Choose the source language code from the original data file
    source_lang_code = 'rus'  # You can dynamically set this based on your needs

    # Translate and save to TOML file
    translate_and_save_to_toml(
        languages=languages,
        input_file_path=input_file_path,
        output_file_path=output_file_path,
        source_lang_code=source_lang_code
    )
