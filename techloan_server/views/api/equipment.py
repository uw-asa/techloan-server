from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import ViewSet
from techloan_server.stf_sql import STFSQL
import logging

logger = logging.getLogger(__name__)


class Equipment(ViewSet):
    @classmethod
    def link(cls, request, pk):
        return reverse('equipment-detail',
                       kwargs={'pk': pk}, request=request)

    @classmethod
    def item(cls, request, record):
        from .equipment_type import EquipmentType

        if request.version == 'v1':
            record.update({
                'uri': cls.link(request, record['id']),
                'equipment_type_uri':
                    EquipmentType.link(request, record['equipment_type_id']),
            })
        else:
            record.update({'_links': {
                'self': {'href': cls.link(request, record['id'])},
                'type': {'href': EquipmentType.link(
                    request, record['equipment_type_id'])},
            }})
        return record

    def list(self, request, **kwargs):
        _stf = STFSQL()
        params = {
            'equipment_id': kwargs.get('equipment_id'),
            'type_id': kwargs.get('type_id'),
        }
        params.update(request.GET)

        items = []

        for record in _stf.equipment(**params):
            items.append(self.item(request, record))

        return Response(items)

    def retrieve(self, request, pk):
        return self.list(request, equipment_id=pk)
