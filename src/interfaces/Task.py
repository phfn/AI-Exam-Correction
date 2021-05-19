#!/usr/bin/env python3

import enum 
import task_types 

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

class Task:

    """Object that describes tasks contained in a document"""

    def __init__(self, number, x, y, width, height, task_type : task_types, expected_answer):
        self.number = number        # Unique ID of task, should represent pos in doc
        self.pos = Point(x, y)      # Position
        self.width = width          
        self.height = height
        self.task_type = task_type  # Type of task, see task_types class for options
        self.expected_answer = expected_answer
        self.actual_answer = ""
         
