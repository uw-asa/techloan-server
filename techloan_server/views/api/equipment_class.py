from rest_framework.response import Response
from techloan_server.stf_sql import STFSQL
from . import TechloanViewSet
import logging

logger = logging.getLogger(__name__)


class EquipmentClass(TechloanViewSet):
    @classmethod
    def item(cls, request, record):
        from .equipment_type import EquipmentType

        if request.version == 'v1':
            record.update({
                'uri': cls.link(request, record['id']),
            })
        else:
            record.update({'_links': {
                'self': {'href': cls.link(request, record['id'])},
                'types': {'href': EquipmentType.search_link(
                    request, class_id=record['id'])},
            }})
        return record

    def list(self, request, **kwargs):
        _stf = STFSQL()
        params = {
            'class_id': kwargs.get('class_id'),
        }
        params.update(request.GET)

        items = []

        for record in _stf.equipment_class(**params):
            item = self.item(request, record)
            items.append(item)

        return Response(items)
