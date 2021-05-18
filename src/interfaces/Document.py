import Task


class Document:

    def __init__(self, document, tasks):
        
        self.clean_document = document # Do not edit
        self.preview_document = document # Document to edit for preview user
        self.tasks = []

    def add_task(self, task : Task):
        self.tasks.append(task)
    
    def sort_tasks_by_pos(self):
        #TODO


