from flask import Flask, request, jsonify, redirect, abort
from flask_caching import Cache

from utils import datastore, openapi


cache = Cache(config={'CACHE_TYPE': 'SimpleCache', "CACHE_DEFAULT_TIMEOUT": 60})

app = Flask(__name__)

cache.init_app(app)


def make_cache_key_from_request(*args, **kwargs):
    args = '&'.join([f'{k}={v}' for k, v in request.args.items()])
    return request.path + '/' + args


@app.route("/")
def home():
    return redirect('/api/', 302)


@app.route("/api/")
@cache.cached()
def list_namespaces():
    namespaces = datastore.list_namespaces()
    return {
        'namespaces': [
            {
                'name': namespace,
                'url': f'/api/{namespace}/',
            }
            for namespace in namespaces
        ],
    }


@app.route("/api/<namespace>/")
@cache.cached()
def get_namespace(namespace):
    kinds = datastore.list_kinds(namespace)
    return {
        'namespace': namespace,
        'kinds': [
            {
                'name': kind,
                'url': f'/api/{namespace}/{kind}',
            }
            for kind in kinds
        ],
        'url_for_openapi_definition': f'/api/{namespace}/openapi.json',
        'url_for_swagger_ui': f'/api/{namespace}/swagger-ui.html',
        'url_for_parent': '/api/',
    }


@app.route("/api/<namespace>/openapi.json")
@cache.cached()
def get_openapi_definition(namespace):
    datastore_schema = datastore.list_properties(namespace)
    openapi_def = openapi.generate_openapi_definition_from_schema(namespace, datastore_schema)
    return openapi_def


@app.route("/api/<namespace>/swagger-ui.html")
@cache.cached()
def get_swagger_ui(namespace):
    openapi_def_url = request.path.replace('swagger-ui.html', 'openapi.json')
    swagger_ui = openapi.SWAGGER_UI
    swagger_ui = swagger_ui.replace('{{ OPEN_API_URL }}', openapi_def_url)
    return swagger_ui


@app.route("/api/<namespace>/<kind>/")
@cache.cached(make_cache_key=make_cache_key_from_request)
def list_entities(namespace, kind):
    filters = request.args.items()
    entities = datastore.list_entities(namespace, kind, filters)
    return {
        'namespace': namespace,
        'kind': kind,
        'entities': entities,
        'url_for_parent': f'/api/{namespace}/',
    }


@app.route("/api/<namespace>/<kind>/<key>")
@cache.cached()
def get_entity(namespace, kind, key):
    entity = datastore.get_entity(namespace, kind, key)
    return entity or abort(404)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
