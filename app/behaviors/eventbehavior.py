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
    def isWeekend(cls, myDate):
        return True if myDate.weekday() == 5 or myDate.weekday() == 6 else False

    def after_put(self, instance):
    	params = {}
        total_hours = instance.total_hours
        alloc_params =  Allocation.find_allocation(instance.allocation_id)
        reflect_hours = Allocation.minusRemaining(alloc_params, total_hours)

        params['name'] = alloc_params.resource_name
        params['email'] = alloc_params.email
        params['project_name'] = alloc_params.project_name
        params['color'] = alloc_params.color
        params['event_id'] = instance.key
        myDate = instance.start_date
        while total_hours > 0:
            if self.isWeekend(myDate) is False:
                conv_date = myDate.strftime('%Y-%m-%d')
                params['start_date'] = conv_date
                params['end'] = conv_date
                if total_hours < instance.frequency:
                    params['summary'] = alloc_params.project_name+" ("+str(total_hours)+")"
                    params['alloc_hours'] = total_hours
                    Allocation.test_call(params)
                else:
                    params['summary'] = alloc_params.project_name+" ("+ str(instance.frequency)+")"
                    total_hours -= instance.frequency
                    params['alloc_hours'] = instance.frequency
                    Allocation.test_call(params)

            myDate += datetime.timedelta(days=1)

