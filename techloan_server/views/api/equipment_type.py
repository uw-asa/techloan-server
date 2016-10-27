from rest_framework.response import Response
from datetime import date
from dateutil.parser import parse
from techloan_server.stf_sql import STFSQL
from . import TechloanViewSet
import logging

logger = logging.getLogger(__name__)


class EquipmentType(TechloanViewSet):
    @classmethod
    def item(cls, request, record):
        from .equipment_class import EquipmentClass
        from .equipment_location import EquipmentLocation
        from .customer_type import CustomerType
        from .availability import Availability
        from .equipment import Equipment

        if request.version == 'v1':
            record.update({
                'uri': cls.link(request, record['id']),
                'equipment_class_uri':
                    EquipmentClass.link(request, record['equipment_class_id']),
                'equipment_location_uri':
                    EquipmentLocation.link(request,
                                           record['equipment_location_id']),
                'customer_type_uri':
                    CustomerType.link(request, record['customer_type_id']),
            })
        else:
            record.update({'_links': {
                'self': {'href': cls.link(request, record['id'])},
                'class': {'href': EquipmentClass.link(
                    request, record['equipment_class_id'])},
                'location': {'href': EquipmentLocation.link(
                    request, record['equipment_location_id'])},
                'customer_type': {'href': CustomerType.link(
                    request, record['customer_type_id'])},
                'availability': {'href': Availability.search_link(
                    request, type_id=record['id'])},
                'equipment': {'href': Equipment.search_link(
                    request, type_id=record['id'])},
            }})
        return record

    def items(self, request, **kwargs):
        from .equipment_class import EquipmentClass
        from .availability import Availability

        _stf = STFSQL()
        params = {
            'type_id': kwargs.get('type_id'),
            'class_id': kwargs.get('class_id'),
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

        for record in _stf.equipment_type(params['type_id'],
                                          params['class_id'],
                                          params['location_id']):
            item = self.item(request, record)
            item['_embedded'] = {}

            if (request.version == 'v1' and params['scope'] == 'extended') or \
                    'class' in params['embed']:
                class_record = list(_stf.equipment_class(
                    record['equipment_class_id']))[0]
                class_item = EquipmentClass.item(request, class_record)
                if request.version == 'v1':
                    item.update({'class': class_item})
                else:
                    item['_embedded'].update({'class': class_item})

            if (request.version == 'v1' and params['scope'] == 'extended') or \
                    'availability' in params['embed']:
                availability_items = []
                for a_record in _stf.availability(params['start_date'],
                                                  params['end_date'],
                                                  record['id']):
                    availability_item = Availability.item(request, a_record)
                    availability_items.append(availability_item)
                if request.version == 'v1':
                    item.update({'availability': availability_items})
                else:
                    item['_embedded'].update(
                        {'availability': availability_items})

            if not len(item['_embedded']):
                del item['_embedded']

            items.append(item)

        return items
