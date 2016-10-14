from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import ViewSet
from techloan_server.stf_sql import STFSQL
import logging

logger = logging.getLogger(__name__)


class EquipmentClass(ViewSet):
    @staticmethod
    def link(request, pk):
        return reverse('equipment-class-detail',
                       kwargs={'pk': pk}, request=request)

    def list(self, request, **kwargs):
        _stf = STFSQL()
        params = {
            'class_id': kwargs.get('class_id'),
        }
        params.update(request.GET)

        records = []

        for record in _stf.equipment_class(**params):
            record.update({
                'uri': self.link(request, record['id']),
            })
            records.append(record)

        return Response(records)

    def retrieve(self, request, pk):
        return self.list(request, class_id=pk)
