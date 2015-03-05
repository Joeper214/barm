from ferris import Controller, messages, route_with
from ferris.components.pagination import Pagination
from app.models.calendar import Calendar

from datetime import timedelta

import json
import datetime


class Calendars(Controller):

    class Meta:
        components = (messages.Messaging, Pagination,)
        Model = Calendar
        pagination_limit = 25
        prefixes = ('api',)

    @route_with('/api/calendars/list', methods=['GET'])
    def api_list(self):
        self.context['data'] = Calendar.list_all()

    @route_with('/api/calendars/create', methods=['POST'])
    def api_create(self):
        params = json.loads(self.request.body)
        hours = int(params['billable_hours'])
        params['billable_hours'] = hours
        params['remaining_hours'] = hours
        params['start_date'] = datetime.datetime.utcfromtimestamp(float(params['start_date']))
        self.context['data'] = Calendar.create(params)

    @route_with('/api/calendars/:<key>', methods=['GET'])
    def api_get(self, key):
        calendar = self.util.decode_key(key).get()
        self.context['data'] = calendar

    @route_with('/api/calendars/:<key>', methods=['POST'])
    def api_update(self, key):
        params = json.loads(self.request.body)
        keyS = self.util.decode_key(params['key']['urlsafe'])
        Calendar.updateHours(params,keyS)

    @route_with('/api/calendars/:<key>', methods=['DELETE'])
    def api_delete(self, key):
        project = self.util.decode_key(key).get()
        project.delete()
        return 200


