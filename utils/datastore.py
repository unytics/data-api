import os

import google.auth
import google.cloud.datastore
from google.cloud.datastore import query as filters



PROJECT = os.environ.get('PROJECT')
DATABASE = os.environ.get('DATABASE')

if not PROJECT:
    _, PROJECT = google.auth.default()


datastore = google.cloud.datastore.Client(project=PROJECT, database=DATABASE)


def list_namespaces():
    query = datastore.query(kind="__namespace__")
    query.keys_only()
    namespaces = ['default'] +  [
        entity.key.id_or_name
        for entity in query.fetch()
        if isinstance(entity.key.id_or_name, str)
    ]
    return namespaces


def list_kinds(namespace):
    if namespace == 'default':
        namespace = None
    query = datastore.query(namespace=namespace, kind="__kind__")
    query.keys_only()
    kinds = [
        entity.key.id_or_name
        for entity in query.fetch()
        if not entity.key.id_or_name.startswith('_')
    ]
    return kinds


def list_properties(namespace, discard_system_kinds=True):
    if namespace == 'default':
        namespace = None
    query = datastore.query(namespace=namespace, kind="__property__")
    properties = {}
    for entity in query.fetch():
        kind = entity.key.parent.name
        if discard_system_kinds and kind.startswith('_'):
            continue
        property_ = {
            'name': entity.key.name,
            'types': entity['property_representation'],
        }
        properties.setdefault(kind, []).append(property_)
    return properties


def list_entities(namespace, kind, filters, limit=100):
    if namespace == 'default':
        namespace = None
    query = datastore.query(namespace=namespace, kind=kind)
    for key, value in filters:
        if not value:
            continue
        query.add_filter(filter=google.cloud.datastore.query.PropertyFilter(key, "=", value))
    entities = [
        {
            **entity,
            **{
                '__key__': entity.key.id_or_name,
                '__url__': f'/api/{namespace or "default"}/{kind}/{entity.key.id_or_name}'
            }
        }
        for entity in query.fetch(limit=limit)
    ]
    return entities


def get_entity(namespace, kind, key):
    if namespace == 'default':
        namespace = None
    datastore_key = datastore.key(kind, key, namespace=namespace)
    entity = datastore.get(datastore_key)
    if entity is None:
        try:
            key = int(key)
            assert key > 0
        except:
            return
        datastore_key = datastore.key(kind, key, namespace=namespace)
        entity = datastore.get(datastore_key)
    if entity is not None:
        entity['__key__'] = datastore_key.id_or_name

    return entity
