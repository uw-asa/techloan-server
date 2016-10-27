from rest_framework.response import Response
from datetime import date
from dateutil.parser import parse
from techloan_server.stf_sql import STFSQL
from . import TechloanViewSet
import logging

logger = logging.getLogger(__name__)


class EquipmentLocation(TechloanViewSet):
    @classmethod
    def item(cls, request, record):
        if request.version == 'v1':
            record.update({
                'uri': cls.link(request, record['id']),
            })
        else:
            record.update({'_links': {
                'self': {'href': cls.link(request, record['id'])},
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
            'embed': [],
        }
        params.update(request.GET)

        if params['start_date'] is str:
            params['start_date'] = parse(params['start_date']).date()
        if params['end_date'] is str:
            params['end_date'] = parse(params['end_date']).date()
        if params['end_date'] < params['start_date']:
            params['end_date'] = params['start_date']

        items = []

        for record in _stf.equipment_location(params['location_id']):
            item = self.item(request, record)
            item['_embedded'] = {}

            if request.version == 'v1' and params['scope'] == 'extended' or \
                    'type' in params['embed']:
                type_items = []
                for type_record in _stf.equipment_type(
                        location_id=params['location_id']):
                    type_item = EquipmentType.item(request, type_record)
                    type_items.append(type_item)
                if request.version == 'v1':
                    item.update({'types': type_items})
                else:
                    item['_embedded'].update({'types': type_items})
            items.append(item)

            if not len(item['_embedded']):
                del item['_embedded']

        return Response(items)
