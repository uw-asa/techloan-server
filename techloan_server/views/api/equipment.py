import logging

from techloan_server.stf_sql import STFSQL

from . import TechloanViewSet

logger = logging.getLogger(__name__)


class Equipment(TechloanViewSet):
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

    def items(self, request, **kwargs):
        _stf = STFSQL()
        params = {
            'equipment_id': kwargs.get('equipment_id'),
            'type_id': kwargs.get('type_id'),
        }
        params.update(request.GET)

        items = []

        for record in _stf.equipment(**params):
            items.append(self.item(request, record))

        return items
