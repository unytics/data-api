import os
from flask import Flask, request, jsonify, redirect, url_for
from flasgger import Swagger
from google.cloud.datastore import query as filters
import google.auth

from utils import doc_generator, transformer
import config


cached_endpoints = []

PROJECT = os.environ.get('PROJECT')


app = Flask(__name__)
app.config["SWAGGER"] = config.SWAGGER_CONF
swagger = Swagger(app, template=config.SWAGGER_TEMPLATE)
datastore = google.cloud.datastore.Client(project=PROJECT)


def query_datastore(resource_name, id, namespace=None):
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
        query.add_filter(filter=filters.PropertyFilter(key, "=", value))
    results = list(query.fetch())    
    return jsonify(results), 200


@app.before_request
def init_app():
    global cached_endpoints
    if cached_endpoints:
        return
        
    query = datastore.query(kind="_schema")
    schema_entities = list(query.fetch())
    
    for result in schema_entities:
        endpoint = result.get("datastore_path", "/api").split('/')[-1]
        columns = [
                dict(column.items()) for column in result.get("columns", [])
            ]
        

        cached_endpoints.append({
            "endpoint_name": f"api/{endpoint}",
            "description": f"Retrieve a list of {endpoint}.",
            "columns": columns,
        })

    schema = doc_generator.generate_openapi_schema(cached_endpoints)
    swagger.template["paths"].update(schema.get('paths'))


@app.route("/")
def hello_world():
    """Example Hello World route."""
    return redirect('/docs')



@app.route("/api/<resource_name>", defaults={"id": None})
@app.route("/api/<resource_name>/<id>")
def list_records(resource_name, id):
    return query_datastore(resource_name, id)

@app.route("<namespace>/api/<resource_name>", defaults={"id": None})
@app.route("<namespace>/api/<resource_name>/<id>")
def list_records_in_namespace(namespace, resource_name, id):
    return query_datastore(resource_name, id, namespace=namespace)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
