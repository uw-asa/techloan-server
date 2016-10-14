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

    def list(self, request, **kwargs):
        from .equipment_class import EquipmentClass
        from .equipment_location import EquipmentLocation
        from .customer_type import CustomerType

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

        records = []

        for record in _stf.equipment_type(params['type_id'],
                                          params['class_id'],
                                          params['location_id']):
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
            if params['scope'] == 'extended':
                class_record = list(_stf.equipment_class(
                    record['equipment_class_id']))[0]
                class_record.update({
                    'uri': EquipmentClass.link(request, class_record['id']),
                })

                availability_records = []
                for a_record in _stf.availability(params['start_date'],
                                                  params['end_date'],
                                                  record['id']):
                    a_record.update({
                        'date_available':
                            a_record['date_available'].strftime('%Y-%m-%d'),
                    })
                    availability_records.append(a_record)
                record.update({
                    'class': class_record,
                    'availability': availability_records,
                })
            records.append(record)

        return Response(records)

    def retrieve(self, request, pk):
        return self.list(request, type_id=pk)
