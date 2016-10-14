from django.core.urlresolvers import get_resolver
from rest_framework.views import APIView
from rest_framework.response import Response
from techloan_server.stf_sql import STFSQL
import logging
import techloan_server.urls

logger = logging.getLogger(__name__)


class Resources(APIView):
    def __init__(self):
        self._stf = STFSQL()

    def get(self, request, **kwargs):
        params = {
        }
        params.update(request.GET)

        resources = []

        def show_urls(urllist, depth=0):
            for entry in urllist:
                resources.append({'depth': depth, 'url': entry.regex.pattern})
                if hasattr(entry, 'url_patterns'):
                    show_urls(entry.url_patterns, depth + 1)

        show_urls(techloan_server.urls.urlpatterns)

        resolver = get_resolver(techloan_server.urls)
        for view, regexes in resolver.reverse_dict.iteritems():
            resources.append({"view": str(view), "regexes": regexes})

        return Response(resources)
