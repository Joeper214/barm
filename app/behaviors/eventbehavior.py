from ferris.core.ndb import Behavior
from app.models.allocation import Allocation
from plugins import calendar
from datetime import timedelta

import json
import datetime

class EventBehavior(Behavior):

    def __init__(self, Model):
        self.Model = Allocation

    def after_delete(self, key):
        pass
    
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

        calendar.create_event('ray.tenorio@sherpademo.com', post)

    @classmethod
    def isWeekend(cls, myDate):
        return True if myDate.weekday() == 5 or myDate.weekday() == 6 else False

    def after_put(self, instance):
    	params = {}
        total_hours = instance.total_hours
        alloc_params =  Allocation.find_allocation(instance.allocation_id)
        reflect_hours = Allocation.minusRemaining(alloc_params, total_hours)

        params['name'] = alloc_params.resource_name
        params['email'] = alloc_params.email
        myDate = instance.start_date
        while total_hours > 0:
            if self.isWeekend(myDate) is False:
                conv_date = myDate.strftime('%Y-%m-%d')
                params['start_date'] = conv_date
                params['end'] = conv_date
                if total_hours < instance.frequency:
                    params['summary'] = alloc_params.project_name+" ("+str(total_hours)+")"
                    self.test_call(params)
                else:
                    params['summary'] = alloc_params.project_name+" ("+ str(instance.frequency)+")"
                    total_hours -= instance.frequency
                    self.test_call(params)

            myDate += datetime.timedelta(days=1)

