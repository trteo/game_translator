from enum import Enum
from typing import Dict


class DeeplSourceLangs(Enum):
    ENGLISH = 'EN'
    RUSSIAN = 'RU'


class FileSourceLangs(Enum):
    ENGLISH = 'eng'
    RUSSIAN = 'rus'


SOURCE_FILE_2_DEEPL_MAP: Dict[FileSourceLangs, DeeplSourceLangs] = {
    FileSourceLangs.ENGLISH: DeeplSourceLangs.ENGLISH,
    FileSourceLangs.RUSSIAN: DeeplSourceLangs.RUSSIAN,
}
