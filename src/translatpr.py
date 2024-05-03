import requests
import toml
from typing import Dict

from settings.config import settings

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

def translate_and_save_to_toml(data: Dict[str, str], languages: Dict[str, str], file_path: str) -> None:
    translations = {}
    for key, value in data.items():
        translations[key] = {}
        for lang_code, lang_name in languages.items():
            translations[key][lang_code.lower()] = translate_text(value, lang_code)

    with open(file_path, "a", encoding="utf-8") as toml_file:
        toml.dump(translations, toml_file)

if __name__ == "__main__":
    # Define your data
    data: Dict[str, str] = {
        "apple": "ROTTING APPLE",
        "banana": "BANANA PEEL",
        "chicken": "GNAWED CHICKEN",
        "fish": "FISH BONES",
        "orange": "ORANGE PEEL"
    }

    # Define languages
    languages: Dict[str, str] = {
        "EN-US": "eng",
        "UK": "ukr",
        "ES": "spa",
        "PT-BR": "pbr",
        "DE": "deu",
        "IT": "ita",
        "TR": "tur"
    }

    # Translate and save to TOML file
    translate_and_save_to_toml(
        data,
        languages,
        "C:\\Users\\f.tropin\\Documents\\work\\perevodichik_ebeyshey_igry\\data\\result\\translations.toml"
    )
