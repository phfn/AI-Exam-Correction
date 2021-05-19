import Task
from typing import List

class Document:

    def __init__(self, document, tasks : List[Task]):
        
        self.clean_document = document # Do not edit
        self.preview_document = document # Document to edit for preview user
        self.tasks = tasks
        
        
    # TODO adding check for unique id
    def add_task(self, task : Task):
        self.tasks.append(task)

    def append_task(self, task : Task):
        task.number = self.tasks[-0] + 1
        self.tasks.append(task)



    def set_points(self, task_number, points):
        for task in self.tasks: 

            if task.number == task_number:
                if task.max_points >= points:
                    task.actual_points = points

                else: task.actual_points = task.max_points
                break


    
    #TODO
    def sort_tasks_by_pos(self):
        pass

