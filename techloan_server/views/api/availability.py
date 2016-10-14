from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from datetime import date, timedelta
from dateutil.parser import parse
from techloan_server.stf_sql import STFSQL
import logging

logger = logging.getLogger(__name__)


class Availability(ViewSet):

    def list(self, request, **kwargs):
        from .equipment_type import EquipmentType

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

        records = []

        for record in _stf.availability(**params):
            record.update({
                'equipment_type_uri':
                    EquipmentType.link(request, record['equipment_type_id']),
                'date_available':
                    record['date_available'].strftime('%Y-%m-%d'),
            })
            records.append(record)

        return Response(records)
