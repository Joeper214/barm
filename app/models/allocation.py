from ferris import BasicModel, ndb
from datetime import datetime, timedelta
from app.models.project import Project
from app.models.calendar import Calendar
from app.behaviors.allocbehavior import AllocBehavior
from plugins import calendar
from datetime import timedelta

import json
import datetime
import logging
import math
import uuid


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

    @classmethod
    def del_by_project_id(cls, key):
        items = cls.find_by_project(key)
        for i in items:
            deferred.defer(cls.del_allocation, i.key.urlsafe())

    @classmethod
    def del_allocation(cls, id):
        key = ndb.Key(urlsafe=id)
        key.delete()

    @classmethod
    def test_call(cls, params):
        owner_email = 'ray.tenorio@sherpademo.com'
        owner_name = 'Ray Tenorio'
        summary = params['summary']
        visibility = 'public'
        description = 'No task specified.'

        post = {}
        post['location'] = ''
        post['creator'] = {}
        post['creator']['email'] = owner_email
        post['creator']['displayName'] = owner_name
        post['organizer'] = {}
        post['organizer']['email'] = owner_email
        post['organizer']['displayName'] = owner_name
        post['summary'] = summary
        post['description'] = description
        post['attendees'] = [{
                'displayName': params['name'],
                'email': params['email'],
                'responseStatus': 'needsAction',
                'organizer': 'false'
                }]
        post['transparency'] = 'opaque'
        post['visibility'] = 'public'
        post['start'] = {}
        post['end'] = {}

        # allday, specific time switch
        post['start']['date'] = params['start_date']
        post['start']['dateTime'] = None

        post['end']['date'] = params['end']
        post['end']['dateTime'] = None

        # reminders
        post['reminders'] = {}
        post['reminders']['useDefault'] = 'true'

        deferred.defer(cls.push_to_calendar, post, params)

    @classmethod
    def push_to_calendar(cls, post, params):
        response = calendar.create_event('ray.tenorio@sherpademo.com', post)
        cal_start = datetime.datetime.strptime(params['start_date'], '%Y-%m-%d')
        cal_end = datetime.datetime.strptime(params['end'], '%Y-%m-%d')
        cal_params = {
            'event_id' : params['event_id'], 
            'calendar_id' : response['id'],
            'alloc_date' : cal_start,
            'alloc_end' : cal_end,
            'alloc_hours' : params['alloc_hours'],
            'project_name' : params['project_name'],
            'color' : params['color'],
            'resource_name' : params['name'],
            'email' : params['email']
        }
        Calendar.create(cal_params)
        

