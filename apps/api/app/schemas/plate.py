from pydantic import BaseModel

ARABIC_TO_ENGLISH: dict[str, str] = {
    'ا': 'A',
    'ب': 'B',
    'ح': 'J',
    'د': 'D',
    'ر': 'R',
    'س': 'S',
    'ص': 'X',
    'ط': 'T',
    'ع': 'E',
    'ق': 'G',
    'ك': 'K',
    'ل': 'L',
    'م': 'Z',
    'ن': 'N',
    'هـ': 'H',
    'و': 'U',
    'ى': 'V',
}

ENGLISH_TO_ARABIC: dict[str, str] = {v: k for k, v in ARABIC_TO_ENGLISH.items()}

VALID_ARABIC_LETTERS: set[str] = set(ARABIC_TO_ENGLISH.keys())
VALID_ENGLISH_LETTERS: set[str] = set(ARABIC_TO_ENGLISH.values())


class PlateEN(BaseModel):
    characters: list[str]
    numbers: list[int]


class PlateAR(BaseModel):
    characters: list[str]
    numbers: list[int]


class Plate(BaseModel):
    en: PlateEN
    ar: PlateAR


class PlateRecognitionResponse(BaseModel):
    plates: list[Plate]
