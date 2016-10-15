from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import ViewSet
from datetime import date
from dateutil.parser import parse
from techloan_server.stf_sql import STFSQL
import logging

logger = logging.getLogger(__name__)


class EquipmentLocation(ViewSet):
    @staticmethod
    def link(request, pk):
        return reverse('equipment-location-detail',
                       kwargs={'pk': pk}, request=request)

    def item(self, request, record):
        if request.version == 'v1':
            record.update({
                'uri': self.link(request, record['id']),
            })
        else:
            record.update({'_links': {
                'self': {'href': self.link(request, record['id'])},
            }})
        return record

    def list(self, request, **kwargs):
        from .equipment_type import EquipmentType

        _stf = STFSQL()
        params = {
            'location_id': kwargs.get('location_id'),
            'start_date': date.today(),
            'end_date': date.today(),
            'scope': 'basic',
        }
        params.update(request.GET.dict())

        if params['start_date'] is str:
            params['start_date'] = parse(params['start_date']).date()
        if params['end_date'] is str:
            params['end_date'] = parse(params['end_date']).date()
        if params['end_date'] < params['start_date']:
            params['end_date'] = params['start_date']

        items = []

        for record in _stf.equipment_location(params['location_id']):
            item = self.item(request, record)
            if params['scope'] == 'extended':
                type_items = []
                for type_record in _stf.equipment_type(
                        location_id=params['location_id']):
                    type_item = EquipmentType.item(type_record)
                    type_items.append(type_item)
                item.update({
                    'types': type_items,
                })
            items.append(item)

        return Response(items)

    def retrieve(self, request, pk):
        return self.list(request, location_id=pk)
