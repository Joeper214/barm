from ferris import Controller, messages, route_with, route
from ferris.components.pagination import Pagination
from app.models.allocation import Allocation
from app.models.project import Project
from app.models.person import Person
from app.models.event import Event
from datetime import timedelta
from plugins import calendar

import json
import datetime
import logging

class Allocations(Controller):
    person = Person()
    project = Project()
    event = Event()

    class Meta:
        components = (messages.Messaging, Pagination,)
        Model = Allocation
        pagination_limit = 25
        prefixes = ('api',)

    @route_with('/')
    def index(self):
        pass

    @route_with('/api/allocations/list', methods=['GET'])
    def api_list(self):
        self.context['data'] = Allocation.list_all()

    @route_with('/api/allocations/:<key>', methods=['GET'])
    def api_get(self, key):
        keyS = self.util.decode_key(key)
        items =  Allocation.find_by_project(keyS)
        self.context['data'] = items

    @route_with('/api/allocations/find/:<key>', methods=['GET'])
    def api_find(self,key):
        items = self.util.decode_key(key).get()
        self.context['data'] = items



    def isWeekend(self, myDate):
        return True if myDate.weekday() == 5 or myDate.weekday() == 6 else False

    def render_google_calendar(self,summary,start,end,attendees):
        calendar_event = {
            'summary' : summary,
            'location' : 'cloudsherpas',
            'start' : { 'dateTime' : start},
            'end' : {'dateTime' : end},
            'attendees' : [{ 'email' : attendees}],
        }
        calendar.create_event('joeper.serrano@sherpademo.com', calendar_event)

    def test_calendar(self):

        event = {'attendees': [{'displayName': 'Cloud Sherpas', 'type': 'lead', 'email': u'joeper.serrano@cloudsherpas.com', 'responseStatus': 'needsAction'}, {'displayName': 'Cloud Sherpas', 'type': 'lead', 'email': u'joeper.serrano@sherpademo.com', 'responseStatus': 'needsAction'}],
            'description': None, 'creator': {'displayName': '', 'email': u'joeper@sherpademo.com'}, 
            'reminders': {'overrides': [{'minutes': 15, 'method': 'popup'}], 
            'useDefault': 'false'}, 
            'visibility': 'public', 
            'summary': u'test nz', 
            'start': {'date': None, 'dateTime': u'2015-03-04T04:00:00.000+0000'}, 
            'location': None, 'transparency': 'opaque', 
            'end': {'date': None, 'dateTime': u'2015-03-04T05:00:00.000+0000'}, 
            'organizer': {'displayName': '', 'email': u'joeper@cloudsherpas.com'}}
        calendar.create_event('joeper.serrano@sherpademo.com', event)

    @route_with('/api/allocations/calendar', methods=['GET'])
    def api_calendar(self):
        allocations = Allocation.list_all()
        events = []
        conv_date = None
        #self.test_calendar()
        for items in allocations:
            load_events = self.event.find_by_allocation(items.key)
            name = items.resource_name
            color = items.color
            proj_name = items.project_name
            email = items.email
            for load in load_events:
                total = load.total_hours
                frequency = load.frequency
                myDate = load.start_date
                #print myDate
                while total > 0:
                    if self.isWeekend(myDate) is False:
                        conv_date = myDate.strftime('%Y-%m-%d')
                        if total < frequency:
                            events += [{'resource_name' : name, 'color' : color, 'project_name' : proj_name, 'alloc_date' : conv_date, 'alloc_hours' : total}]               
                        else:
                            events += [{'resource_name' : name, 'color' : color, 'project_name' : proj_name, 'alloc_date' : conv_date, 'alloc_hours' : frequency}]
                            total -= frequency
                    myDate += datetime.timedelta(days=1)
        #self.render_google_calendar('Test',conv_date,conv_date,'joeper.serrano@cloudsherpas.com')
        return json.dumps(events)



    @route_with('/api/allocations/create', methods=['POST'])
    def api_create(self):
        params = json.loads(self.request.body)
        key = self.util.decode_key(params['project_id']['urlsafe'])
        name = params['name']
        alloc_hours = int(params['alloc_hours'][0])
        per = self.person.find_by_name(params['resource_name'][0])
        res = Allocation.find_by_resource_name(params['resource_name'][0])
        print res
        info = {'project_id' : key,
                'total_hours' : alloc_hours,
                'project_name' : name,
                'remaining_hours' : alloc_hours,
                'temp_alloc' : alloc_hours}
        if res is not None and res.project_name == name:
            Allocation.updateRemaining(res,alloc_hours)
        else:
            if per is not None:
                info['resource_name'] = per.name
                info['color'] = per.color
                info['email'] = per.email
            else:
                person_params = {'name' : params['resource_name'][0], 'color' : params['color'][0], 'email' : params['email'][0]}
                self.person.create(person_params)
                info['resource_name'] = params['resource_name'][0]
                info['color'] = params['color'][0]
                info['email'] = params['email'][0]
                
            Allocation.create(info)
        return 200

    @route_with('/api/allocations/:<key>', methods=['DELETE'])
    def api_delete(self, key):
        items = self.util.decode_key(key).get()
        alloc_id = self.util.decode_key(key)
        retHour = items.total_hours
        retID = items.project_id
        retData = Project.find_by_proj_key(retID)
        print retData
        Project.retHours(retData, retHour)
        items.delete()
        self.event.delete_by_alloc_id(alloc_id)
        return 200
        # self.context['data'] = Allocation.create(params)