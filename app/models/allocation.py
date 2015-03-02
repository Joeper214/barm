from ferris import BasicModel, ndb
from datetime import datetime, timedelta
from app.models.project import Project
from app.behaviors.allocbehavior import AllocBehavior
import math

class Allocation(BasicModel):
    project_id = ndb.KeyProperty()
    project_name = ndb.StringProperty() #temporarily store project_name
    color = ndb.StringProperty() #temporarily store color
    resource_name = ndb.StringProperty()
    email = ndb.StringProperty()
    total_hours = ndb.FloatProperty()
    remaining_hours = ndb.FloatProperty()
    temp_alloc = ndb.FloatProperty()
    temp_type = ndb.StringProperty(default='')

    class Meta:
        behaviors = (AllocBehavior, )

    @classmethod
    def list_all(cls):
        return cls.query().order(cls.resource_name).fetch()

    @classmethod
    def create(cls, params):
        item = cls()
        item.populate(**params)
        item.put()
        return item

    @classmethod
    def find_by_alloc_key(cls, key):
        return cls.query(cls.key == key).fetch()


    @classmethod
    def get(cls, key):
        return cls(parent=key)

    @classmethod
    def find_allocation(cls, key):
        return key.get()

    @classmethod
    def minusRemaining(self, params, hours):
        params.remaining_hours -= float(hours)
        params.temp_type = 'minus'
        params.put()
    @classmethod
    def retHours(self,params, hours):
        print params[0]
        params[0].remaining_hours += float(hours)
        params[0].temp_type = 'return'
        params[0].put()

    @classmethod
    def updateRemaining(self, data, all_hours):
        data.remaining_hours+=all_hours
        data.total_hours+=all_hours
        data.temp_alloc=all_hours
        data.temp_type = 'update'
        data.put()

    @classmethod
    def find_by_project(cls, id):
        return cls.query().filter(cls.project_id == id).fetch()

    def delete(self):
        ndb.delete_multi(ndb.Query(ancestor=self.key).iter(keys_only=True))
