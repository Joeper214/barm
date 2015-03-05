from ferris import BasicModel, ndb
from app.behaviors.taskbehavior import TaskBehavior


class Task(BasicModel):
    taskContent = ndb.StringProperty()
    calendar_id = ndb.StringProperty()

    class Meta:
        behaviors = (TaskBehavior, )

    @classmethod
    def list_all(cls):
        return cls.query().order(cls.calendar_id)

    @classmethod
    def find_by_task_id(cls, task_id):
        return cls.query().filter(cls.key == task_id)

    @classmethod
    def get(cls, key):
        return cls(parent=key)

    @classmethod
    def update(self, params):
        self.populate(**params)
        self.put()

    @classmethod
    def updateTaskContent(self, key, params):
        data = self.query(self.key == key).fetch()
        print repr(data)
        data[0].taskContent=params['taskContent']
        data[0].put()


    @classmethod
    def create(cls, params):
        item = cls()
        item.populate(**params)
        item.put()
        return item
