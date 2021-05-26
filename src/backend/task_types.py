import enum


class Task_type(enum.Enum):

    SINGLE_CHOICE = 0
    MULTIPLE_CHOICE = 1
    NUMBER = 2
    TEXT = 3
    TEXT_NO_NUMBERS = 4
    SHAPE = 5
