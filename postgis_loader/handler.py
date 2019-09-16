#  Copyright (C) 2017 Atelier Cartographique <contact@atelier-cartographique.be>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, version 3 of the License.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import io
import codecs
from json import loads, dump
from django.core.cache import caches, InvalidCacheBackendError
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, JsonResponse, FileResponse
from django.views.decorators.http import require_http_methods
from .serializer import get_geojson


def handle_request(request, schema, table):

    user = request.user
    if not user.has_perm('postgis_loader', (schema, table)):
        raise PermissionDenied()

    try:
        cache = caches['layers']
        ckey = '{}.{}'.format(schema, table)
        try:
            reader = cache.read(ckey)
            reader_type = type(reader)
            # print('ReaderType {} {}'.format(ckey, reader_type))
            if reader_type is io.BufferedReader:
                return FileResponse(reader, content_type='application/json')
            elif reader_type is dict:
                return JsonResponse(reader)

            response = HttpResponse(reader, content_type='application/json')
            return response

        except KeyError:
            # there's been of juggling to force diskcache
            # to return a BufferedReader from cache.read
            stream = io.BytesIO()
            writer = codecs.getwriter("utf-8")(stream)
            data = get_geojson(schema, table)
            dump(data, writer)
            stream.seek(0)
            cache.set(ckey, stream, read=True)
            return JsonResponse(data)

    except InvalidCacheBackendError:
        print('InvalidCacheBackendError')
        return HttpResponse(
            content=get_geojson(schema, table),
            content_type='application/json')
