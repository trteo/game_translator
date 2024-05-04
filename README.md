# perevodichik_ebeyshey_igry

### Requirements
```
ЭВМ

python 3.9
pyenv
poetry
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