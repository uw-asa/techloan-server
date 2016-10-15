from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import ViewSet
from datetime import date
from dateutil.parser import parse
from techloan_server.stf_sql import STFSQL
import logging

logger = logging.getLogger(__name__)


class EquipmentType(ViewSet):
    @staticmethod
    def link(request, pk):
        return reverse('equipment-type-detail',
                       kwargs={'pk': pk}, request=request)

    def item(self, request, record):
        from .equipment_class import EquipmentClass
        from .equipment_location import EquipmentLocation
        from .customer_type import CustomerType

        if request.version == 'v1':
            record.update({
                'uri': self.link(request, record['id']),
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
                'self': {'href': self.link(request, record['id'])},
                'class': {'href': EquipmentClass.link(
                    request, record['equipment_class_id'])},
                'location': {'href': EquipmentLocation.link(
                    request, record['equipment_location_id'])},
                'customer_type': {'href': CustomerType.link(
                    request, record['customer_type_id'])},
            }})
        return record

    def list(self, request, **kwargs):
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
        }
        params.update(request.GET.dict())

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
            if params['scope'] == 'extended':
                class_record = list(_stf.equipment_class(
                    record['equipment_class_id']))[0]
                class_item = EquipmentClass.item(request, class_record)

                availability_items = []
                for a_record in _stf.availability(params['start_date'],
                                                  params['end_date'],
                                                  record['id']):
                    availability_item = Availability.item(request, a_record)
                    availability_items.append(availability_item)
                item.update({
                    'class': class_item,
                    'availability': availability_items,
                })
            items.append(item)

        return Response(items)

    def retrieve(self, request, pk):
        return self.list(request, type_id=pk)
