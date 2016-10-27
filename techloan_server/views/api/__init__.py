import logging
from urllib import urlencode
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import ViewSet
from rest_framework.views import get_view_name
from techloan_server.stf_sql import STFSQL

logger = logging.getLogger(__name__)


def remove_leading_string(content, leading):
    """
    Strip leading component `leading` from `content` if it exists.
    Used when generating names from view classes.
    """
    if content.startswith(leading) and content != leading:
        return content[len(leading):]
    return content


class TechloanViewSet(ViewSet):
    @classmethod
    def base_name(cls):
        name = get_view_name(cls)
        name = name.lower()
        name = name.replace(' ', '-')
        return name

    @classmethod
    def sql_name(cls):
        name = get_view_name(cls)
        name = name.lower()
        name = name.replace(' ', '_')
        return name

    @classmethod
    def pk_name(cls):
        name = cls.sql_name()
        name = remove_leading_string(name, 'equipment_')
        return "%s_id" % name

    @classmethod
    def search_link(cls, request, **kwargs):
        return reverse('%s-list' % cls.base_name(), request=request) + \
               "?%s" % urlencode(kwargs, True)

    @classmethod
    def link(cls, request, pk):
        return reverse('%s-detail' % cls.base_name(),
                       kwargs={'pk': pk}, request=request)

    def retrieve(self, request, pk, **kwargs):
        params = {self.pk_name(): pk}
        return self.list(request, **params)

    def items(self, request, **kwargs):
        _stf = STFSQL()
        params = {
            self.pk_name(): kwargs.get(self.pk_name()),
        }
        params.update(request.GET)

        items = []

        sql_method = getattr(_stf, self.sql_name())
        for record in sql_method(params[self.pk_name()]):
            item = self.item(request, record)
            items.append(item)

        return items

    def list(self, request, **kwargs):
        return Response(self.items(request, **kwargs))
