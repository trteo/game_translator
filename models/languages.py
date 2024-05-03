from enum import Enum
from typing import Dict


class SourceLangsCodes(Enum):
    RUSSIAN = 'rus'
    ENGLISH = 'eng'
    UKRAINE = 'ukr'
    SPANISH = 'spa'
    PORTUGUESE_BRAZILIAN = 'pbr'

    GERMAN = 'deu'
    ITALIAN = 'ita'
    TURKISH = 'tur'


class DeeplLangsCodes(Enum):
    RUSSIAN = 'ru'
    ENGLISH = 'en-us'
    UKRAINE = 'uk'
    SPANISH = 'es'
    PORTUGUESE_BRAZILIAN = 'pt-br'

    GERMAN = 'de'
    ITALIAN = 'it'
    TURKISH = 'tr'


SOURCE_FILE_2_DEEPL_MAP: Dict[SourceLangsCodes, str] = {
    SourceLangsCodes.RUSSIAN: DeeplLangsCodes.RUSSIAN.value,
    SourceLangsCodes.ENGLISH: DeeplLangsCodes.ENGLISH.value,
}


DEEPL_2_SOURCE_FILE_MAP: Dict[str, str] = {
    DeeplLangsCodes.RUSSIAN.value: SourceLangsCodes.RUSSIAN.value,
    DeeplLangsCodes.ENGLISH.value: SourceLangsCodes.ENGLISH.value,
    DeeplLangsCodes.UKRAINE.value: SourceLangsCodes.UKRAINE.value,
    DeeplLangsCodes.SPANISH.value: SourceLangsCodes.SPANISH.value,
    DeeplLangsCodes.PORTUGUESE_BRAZILIAN.value: SourceLangsCodes.PORTUGUESE_BRAZILIAN.value,
    DeeplLangsCodes.GERMAN.value: SourceLangsCodes.GERMAN.value,
    DeeplLangsCodes.ITALIAN.value: SourceLangsCodes.ITALIAN.value,
    DeeplLangsCodes.TURKISH.value: SourceLangsCodes.TURKISH.value,
}
