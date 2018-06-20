#
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

from django.conf import settings
from django.db import connections
from .models import get_layer

GEOJSON_QUERY = """
SELECT row_to_json(fc)
  FROM (
    SELECT 
      'FeatureCollection' AS type, 
      array_to_json(array_agg(f)) AS features
    FROM (
        SELECT 
          'Feature' AS type, 
          ST_AsGeoJSON(sd.{geometry_column}, {max_decimal_digits})::json AS geometry,
          {pk_column} as id, 
          row_to_json((
            SELECT prop FROM (SELECT {field_names}) AS prop
           )) AS properties
        FROM "{schema}"."{table}" AS sd 
    ) AS f 
  ) AS fc;
"""


def get_query(schema, table):
    model, geometry_field, geometry_field_type = get_layer(schema, table)
    fields = []
    for field in model._meta.get_fields():
        if field.get_attname() != geometry_field:
            fields.append('"{}"'.format(field.column))
    pk_field = model._meta.pk.column

    return GEOJSON_QUERY.format(
        pk_column=pk_field,
        schema=schema,
        table=table,
        max_decimal_digits=getattr(settings, 'MAX_DECIMAL_DIGITS', 2),
        geometry_column=geometry_field,
        field_names=', '.join(fields))


def get_geojson(schema, table):
    query = get_query(schema, table)
    with connections[schema].cursor() as cursor:
        cursor.execute(query)
        row = cursor.fetchone()

    return row[0]


def get_model(schema, table):
    model, geometry_field, geometry_field_type = get_layer(schema, table)

    return model
