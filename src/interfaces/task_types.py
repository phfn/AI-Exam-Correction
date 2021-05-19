import enum


class Task_type(enum.Enum):

    single_choice = 0
    multiple_choice = 1
    number = 2
    text = 3
    text_no_numbers = 4
    shape = 5
