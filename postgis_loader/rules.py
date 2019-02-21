from rules import (add_perm, predicate)
from api.models import (
        UserMap,
        MetaData,
    )
from api.rules import (
        is_map_author,
        is_public_map,
        map_group_intersects,
        )


def layer_uri(schema, table_name):
    return 'postgis://{}/{}'.format(schema, table_name)

def get_maps_for_layer(uri):
    md = MetaData.objects.get(resource_identifier=uri)
    return UserMap.objects.filter(layers__metadata=md.id)

@predicate
def is_layer_author(user, layer):
    maps = get_maps_for_layer(layer_uri(*layer))
    for m in maps:
        if is_map_author(user, m):
            return True
    return False


@predicate
def layer_group_intersects(user, layer):
    maps = get_maps_for_layer(layer_uri(*layer))
    for m in maps:
        if map_group_intersects(user, m):
            return True
    return False


@predicate
def is_public_layer(user, layer):
    maps = get_maps_for_layer(layer_uri(*layer))
    for m in maps:
        if is_public_map(user, m):
            return True
    return False


def hook():
    add_perm(
        'postgis_loader', 
        is_layer_author
        | layer_group_intersects 
        | is_public_layer
     )
