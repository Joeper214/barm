from ferris.core.ndb import Behavior
from app.models.allocation import Allocation

class ProjectBehavior(Behavior):
    def __init__(self, Model):
        self.Model = (Allocation,)

    def after_delete(self, key):
        Allocation.del_by_project_id(key)
        pass

    def after_put(self, instance):
        pass


