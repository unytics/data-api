import os
from flask import Flask, request, jsonify
from flasgger import Swagger
from google.cloud.datastore import query as filters
import google.auth
from collections import defaultdict

from utils import doc_generator, transformer
import config


cached_endpoints = []

PROJECT = os.environ.get('PROJECT')


app = Flask(__name__)
app.config["SWAGGER"] = config.SWAGGER_CONF
swagger = Swagger(app, template=config.SWAGGER_TEMPLATE)
datastore = google.cloud.datastore.Client(project=PROJECT)


@app.before_request
def init_app():
    global cached_endpoints
    if cached_endpoints:
        return
    
    query = datastore.query(namespace="_schema")
    schema_entities = list(query.fetch())
    kinds = defaultdict(dict)

    for schema_entity in schema_entities:
        kind = schema_entity.key.kind
        field_name = schema_entity["name"]
        field_type = schema_entity["type"]
        kinds[kind][field_name] = field_type

    for kind, fields in kinds.items():
        cached_endpoints.append({
            "endpoint_name": f"api/{kind}",
            "description": f"Retrieve a list of {kind}.",
            "columns": fields,
        })

    schema = doc_generator.generate_openapi_schema(cached_endpoints)
    swagger.template["paths"].update(schema.get('paths'))


@app.route("/")
def hello_world():
    """Example Hello World route."""
    return f"Hello paul!"


@app.route("/api/<resource_name>", defaults={"id": None})
@app.route("/api/<resource_name>/<id>")
def list_records(resource_name, id):
    if id:
        key = datastore.key(resource_name, transformer.string2number(id))
        entity = datastore.get(key)
        if entity:
            return jsonify(entity), 200
        else:
            return jsonify({"error": "Entity not found"}), 404
            
    query = datastore.query(kind=resource_name)

    for key, value in request.args.items():
        if not value:
            continue
        value = transformer.string2number(value)
        query.add_filter(filter=filters.PropertyFilter(key, "=", value))
    results = list(query.fetch())
    return jsonify(results), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
