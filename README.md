# Game files translator

### Supported languages
* Russian
* English
* Ukraine
* Spanish
* Portuguese_brazilian
* German
* Italian
* Turkish

### Supported files types and structures

#### .toml
``` 

```

#### .rpy
``` 

```

#### .txt
``` 

```


### Requirements
```
ЭВМ

python 3.9
pyenv
poetry
```

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
1. Скопировать `/settings/env.example`в `/settings/env`
2. Задать значение `DEEPL_API_KEY` вашим ключом для Deepl API
3. Запустить `python .\main.py` from project root
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
