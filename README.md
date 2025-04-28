# Game files translator

## Features

A program that translates game files from Russian into a target language using OpenAI API and DeepL API.

## Key Technologies
* **Pydantic Settings** (^2.2.1) – Application configuration management.
* **Requests** (^2.31.0) – Integration with the DeepL translator.
* **OpenAI** (^1.37.0) – Interaction with ChatGPT API.

## Requirements
python 3.9
pyenv
poetry

### Supported languages
* Russian
* English
* Ukraine
* Spanish
* Portuguese_brazilian
* German
* Italian
* Turkish


### Requirements install macos
```bash
# if no homebreww

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
(echo; echo 'eval "$(/opt/homebrew/bin/brew shellenv)"') >> /Users/fedortropin/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"

brew install poetry
brew install pyenv
```


### Install
``` shell
pyenv install 3.9.0
pyenv local 3.9.0
poetry shell
poetry install

```

### Run
1. Copy `/settings/env.example` to `/settings/env`
2. Set env values:  
   1. `DEEPL_API_KEY` - for run translation with DeepL API
   2. `OPENAI_ORG_ID`, `PROJECT_ID`, `CHAT_GPT_API_KEY` - for ChatGPT translation
3. Run `python .\main.py` from project root
4. In  `main.py` `TranslationService(source_lang_code=...)`  `SourceLangsCodes` can be set to 
`SourceLangsCodes.RUSSIAN` or `SourceLangsCodes.ENGLISH` to use base translate if you want to chose language.
5. `python .\main.py`


Языки для перевода задаются в `models/languages.py` и должны быть согласованы с доступными в deepl


### Project structure
`/base/` - Базовые абстрактные классы \
`/data/` - Файлы с изначальным текстом и результатом переводов \
`/models/` - Описание структур данных, константы и их маппинги \
`/settings/` - Переменные окружения, конфигурация логгера \
`/src/translators/chatgpt/` - Перевод файлов при помощи апи ChatGPT \
`/src/translators/deepl/` -  Перевод файлов при помощи апи deepl



##### Разработчик
Тропин Федор \
tg: **@fedorTrop**