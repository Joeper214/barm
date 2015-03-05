from ferris import BasicModel, ndb
from datetime import datetime, timedelta
from google.appengine.ext import deferred


class Calendar(BasicModel):
    event_id = ndb.KeyProperty(required=True)
    calendar_id = ndb.StringProperty(required=True)
    alloc_date = ndb.DateProperty(required=True)
    alloc_end = ndb.DateProperty(required=True)
    alloc_hours = ndb.FloatProperty(required=True)
    project_name = ndb.StringProperty(required=True)
    resource_name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    color = ndb.StringProperty(required=True)

    # class Meta:
    #     behaviors = (EventBehavior, )

    @classmethod
    def list_all(cls):
        return cls.query().order(cls.alloc_date).fetch()

    @classmethod
    def get(cls, key):
        return cls(parent=key)

    @classmethod
    def create(cls, params):
        item = cls()
        item.populate(**params)
        item.put()
        return item

    def update(self, params):
        self.populate(**params)
        self.put()
    
    @classmethod
    def find_by_allocation(cls, id):
        return cls.query().filter(cls.allocation_id == id).order(cls.end_date).fetch()

    def delete(self):
        ndb.delete_multi(ndb.Query(ancestor=self.key).iter(keys_only=True))

    @classmethod
    def delete_by_alloc_id(cls,id):
        allocs = cls.find_by_allocation(id)
        for a in allocs:
            deferred.defer(cls.del_events, a.key.urlsafe())

    @classmethod
    def del_events(cls, key):
        key = ndb.Key(urlsafe=key)
        key.delete()
