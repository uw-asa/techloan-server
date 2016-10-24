from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import ViewSet
from datetime import date, timedelta
from dateutil.parser import parse
from urllib import urlencode
from techloan_server.stf_sql import STFSQL
import logging

logger = logging.getLogger(__name__)


class Availability(ViewSet):
    @classmethod
    def search_link(cls, request, **kwargs):
        return reverse('availability-list', request=request) + \
               "?%s" % urlencode(kwargs, True)

    @classmethod
    def item(cls, request, record):
        from .equipment_type import EquipmentType

        record.update({
            'date_available':
                record['date_available'].strftime('%Y-%m-%d'),
        })
        if request.version == 'v1':
            record.update({
                'equipment_type_uri':
                    EquipmentType.link(request, record['equipment_type_id']),
            })
        else:
            record.update({'_links': {
                'type': {'href': EquipmentType.link(
                    request, record['equipment_type_id'])},
            }})

        return record

    def list(self, request, **kwargs):
        _stf = STFSQL()
        params = {
            'start_date': date.today(),
            'end_date': date.today() + timedelta(weeks=2),
        }
        params.update(request.GET)

        if params['start_date'] is str:
            params['start_date'] = parse(params['start_date']).date()
        if params['end_date'] is str:
            params['end_date'] = parse(params['end_date']).date()

        availability_items = []

        for record in _stf.availability(**params):
            availability_item = self.item(request, record)
            availability_items.append(availability_item)

        if request.version == 'v1':
            return Response(availability_items)

        search = {
            '_links': {'self': {'href': self.search_link(request, **params)}},
            '_embedded': {'availability': availability_items},
        }

        return Response(search)
