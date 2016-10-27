from rest_framework.response import Response
from techloan_server.stf_sql import STFSQL
from . import TechloanViewSet
import logging

logger = logging.getLogger(__name__)


class CustomerType(TechloanViewSet):
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
            'customer_type_id': kwargs.get('customer_type_id'),
        }
        params.update(request.GET)

        items = []

        for record in _stf.customer_type(params['customer_type_id']):
            item = self.item(request, record)
            items.append(item)

        return Response(items)
