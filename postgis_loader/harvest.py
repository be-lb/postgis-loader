from json import dumps

from django.db import connections
from django.http import JsonResponse

from .serializer import get_query

HARVEST_QUERY = """
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
        WHERE ST_Intersects(sd.{geometry_column}, ST_GeomFromGeoJSON('{geometry_request}'))
    ) AS f 
  ) AS fc;
"""


def harvest(rid, geometry_data):
    """
    ...
    """
    schema = rid.hostname
    table = rid.path[1:]

    geometry_string = dumps(geometry_data)
    query = get_query(
        schema, table, HARVEST_QUERY, geometry_request=geometry_string)

    with connections[schema].cursor() as cursor:
        cursor.execute(query)
        row = cursor.fetchone()

    fc = row[0]
    if fc['features'] is None:
        fc['features'] = []

    return JsonResponse(fc)
