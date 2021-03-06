from ferris.core.ndb import Behavior
from app.models.project import Project
# from app.models.event import Event 

class AllocBehavior(Behavior):
    def __init__(self, Model):
        self.Model = (Project,)

    def after_delete(self, key):
        pass

    def after_put(self, instance):
        total_hours = instance.temp_alloc
        alloc_id = instance.key
        if instance.temp_type == 'minus' or instance.temp_type == 'return':
            pass
        else:
            proj_params = Project.find_by_proj_key(instance.project_id)
            rem_hours = Project.removeHours(proj_params, total_hours)
            pass


