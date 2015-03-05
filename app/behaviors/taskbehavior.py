from ferris.core.ndb import Behavior
from app.models.project import Project
from plugins import calendar

class TaskBehavior(Behavior):
    def __init__(self, Model):
        self.Model = (Project,)

    def after_delete(self, key):
        pass


    @classmethod
    def updateTask(self,id,task):
        response = calendar.get_event_by_id('ray.tenorio@sherpademo.com',id)
        print response
        response['description'] = task

        calendar.update_event( id,'ray.tenorio@sherpademo.com',response)

    def after_put(self, instance):
        calendar_id = instance.calendar_id
        taskContent = instance.taskContent

        self.updateTask(calendar_id,taskContent)


