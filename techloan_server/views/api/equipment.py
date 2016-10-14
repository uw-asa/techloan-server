from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import ViewSet
from techloan_server.stf_sql import STFSQL
import logging

logger = logging.getLogger(__name__)


class Equipment(ViewSet):
    @staticmethod
    def link(request, pk):
        return reverse('equipment-detail',
                       kwargs={'pk': pk}, request=request)

    def list(self, request, **kwargs):
        from .equipment_type import EquipmentType

        _stf = STFSQL()
        params = {
            'equipment_id': kwargs.get('equipment_id'),
            'type_id': kwargs.get('type_id'),
        }
        params.update(request.GET)

        records = []

        for record in _stf.equipment(**params):
            record.update({
                'uri': self.link(request, record['id']),
                'equipment_type_uri':
                    EquipmentType.link(request, record['equipment_type_id']),
            })
            records.append(record)

        return Response(records)

    def retrieve(self, request, pk):
        return self.list(request, equipment_id=pk)
