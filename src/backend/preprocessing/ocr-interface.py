from Document import Document
from Task import Task
from task_types import task_type
from checkboxchecker import find_checkboxes
from PIL import Image

def check_document(doc : Document):
   for task : Task in doc.tasks:

        if task.type == Task_type.SINGLE_CHOICE:
            result, doc.img_modified = find_checkboxes(doc.img.crop(task.x, task.y, task.x + task.width, task.y + task.height))
            task.actual_answer = result
            
        elif task.type == Task_typ.MULTIPLE_CHOICE:
            result, doc.img_modified = find_checkboxes(doc.img.crop(task.x, task.y, task.x + task.width, task.y + task.height))
            task.actual_answer = result

    
    return doc