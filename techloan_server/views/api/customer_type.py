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
