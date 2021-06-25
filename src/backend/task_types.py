import enum


class Task_type(enum.Enum):

    SINGLE_CHOICE = 0
    MULTIPLE_CHOICE = 1
    NUMBER = 2
    TEXT = 3
    TEXT_NO_NUMBERS = 4
    SHAPE = 5


def from_str(s: str):
    a = {
        "SINGLE_CHOICE" : Task_type.SINGLE_CHOICE,
        "MULTIPLE_CHOICE" : Task_type.MULTIPLE_CHOICE,
        "NUMBER" : Task_type.NUMBER,
        "TEXT" : Task_type.TEXT,
        "TEXT_NO_NUMBERS" : Task_type.TEXT_NO_NUMBERS,
        "SHAPE" : Task_type.SHAPE
    }
    return a[s.upper().replace(" ", "_")]
