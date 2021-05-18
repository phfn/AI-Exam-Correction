#!/usr/bin/env python3

import enum 


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

class Task:

    """Object that describes tasks contained in a document"""

    def __init__(self, number, x, y, width, height, task_type, expected_answer):
        self.number = number 
        self.pos = Point(x, y)
        self.width = width
        self.height = height
        self.task_type = task_type
        self.expected_answer = expected_answer
        self.actual_answer = ""
         
