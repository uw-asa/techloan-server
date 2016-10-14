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

    def list(self, request, **kwargs):
        from .equipment_type import EquipmentType
        from .equipment_class import EquipmentClass

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

        records = []

        for record in _stf.equipment_location(params['location_id']):
            record.update({
                'uri': self.link(request, record['id']),
            })
            if params['scope'] != 'extended':
                records.append(record)
                continue

            type_records = []
            for type_record in _stf.equipment_type(
                    location_id=params['location_id']):
                availability_records = []

                for a_record in _stf.availability(params['start_date'],
                                                  params['end_date'],
                                                  type_record['id']):
                    a_record.update({
                        'date_available':
                            a_record['date_available'].strftime('%Y-%m-%d'),
                    })
                    availability_records.append(a_record)

                type_record.update({
                    'uri': EquipmentType.link(request, type_record['id']),
                    'equipment_class_uri':
                        EquipmentClass.link(request,
                                            type_record['equipment_class_id']),
                    'availability': availability_records,
                })
                type_records.append(type_record)
            record.update({
                'types': type_records,
            })
            records.append(record)

        return Response(records)

    def retrieve(self, request, pk):
        return self.list(request, location_id=pk)
