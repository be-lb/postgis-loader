def hook(rules):
    rules.add_perm(
        'postgis_loader', rules.is_layer_author
        | rules.layer_group_intersects | rules.is_public_layer)
