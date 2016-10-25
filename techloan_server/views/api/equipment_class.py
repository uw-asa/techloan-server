from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import ViewSet
from techloan_server.stf_sql import STFSQL
import logging

logger = logging.getLogger(__name__)


class EquipmentClass(ViewSet):
    @classmethod
    def link(cls, request, pk):
        return reverse('equipment-class-detail',
                       kwargs={'pk': pk}, request=request)

    @classmethod
    def item(cls, request, record):
        if request.version == 'v1':
            record.update({
                'uri': cls.link(request, record['id']),
            })
        else:
            record.update({'_links': {
                'self': {'href': cls.link(request, record['id'])},
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

    def retrieve(self, request, pk, **kwargs):
        return self.list(request, class_id=pk)
