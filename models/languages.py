from enum import Enum
from typing import Dict, Optional

from pydantic import BaseModel


class SourceLangsCodes(Enum):
    RUSSIAN = 'rus'
    ENGLISH = 'eng'
    UKRAINE = 'ukr'
    SPANISH = 'spa'
    PORTUGUESE_BRAZILIAN = 'pbr'

    GERMAN = 'deu'
    ITALIAN = 'ita'
    TURKISH = 'tur'


class DeeplLangCodesMapping(BaseModel):
    source: Optional[str]
    target: str


class DeeplLangsCodes(Enum):
    RUSSIAN = DeeplLangCodesMapping(source='ru', target='ru')
    ENGLISH = DeeplLangCodesMapping(source='en', target='en-us')
    UKRAINE = DeeplLangCodesMapping(source=None, target='uk')
    SPANISH = DeeplLangCodesMapping(source=None, target='es')
    PORTUGUESE_BRAZILIAN = DeeplLangCodesMapping(source=None, target='pt-br')
    GERMAN = DeeplLangCodesMapping(source=None, target='de')
    ITALIAN = DeeplLangCodesMapping(source=None, target='it')
    TURKISH = DeeplLangCodesMapping(source=None, target='tr')


SOURCE_FILE_2_DEEPL_MAP: Dict[SourceLangsCodes, str] = {
    SourceLangsCodes.RUSSIAN: DeeplLangsCodes.RUSSIAN.value.source,
    SourceLangsCodes.ENGLISH: DeeplLangsCodes.ENGLISH.value.source,
}


DEEPL_2_SOURCE_FILE_MAP: Dict[str, str] = {
    DeeplLangsCodes.RUSSIAN.value.target: SourceLangsCodes.RUSSIAN.value,
    DeeplLangsCodes.ENGLISH.value.target: SourceLangsCodes.ENGLISH.value,
    DeeplLangsCodes.UKRAINE.value.target: SourceLangsCodes.UKRAINE.value,
    DeeplLangsCodes.SPANISH.value.target: SourceLangsCodes.SPANISH.value,
    DeeplLangsCodes.PORTUGUESE_BRAZILIAN.value.target: SourceLangsCodes.PORTUGUESE_BRAZILIAN.value,
    DeeplLangsCodes.GERMAN.value.target: SourceLangsCodes.GERMAN.value,
    DeeplLangsCodes.ITALIAN.value.target: SourceLangsCodes.ITALIAN.value,
    DeeplLangsCodes.TURKISH.value.target: SourceLangsCodes.TURKISH.value,
}
