import os
import json

from flask import Flask, request, jsonify
from flasgger import Swagger
import google.cloud.datastore
from google.cloud.datastore import query as filters
from utils import doc_generator, transformer
import config

import google.auth

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
    print('load endpoints/schema from datastore')
    cached_endpoints = [
        {
            "endpoint_name": "api/getUsers",
            "description": "Retrieve a list of users.",
            "columns": {
                "username": "string",
                "email": "string",
                "age": "integer"
            }
        },
        {
            "endpoint_name": "api/getProducts",
            "description": "Retrieve a list of products.",
            "columns": {
                "productName": "string",
                "price": "number",
                "inStock": "boolean"
            }
        }
    ]

    schema = doc_generator.generate_openapi_schema(cached_endpoints)
    swagger.template["paths"].update(schema.get('paths'))


@app.route("/")
def hello_world():
    """Example Hello World route."""
    return f"Hello paul!"



@app.route("/api/<resource_name>")
def list_records(resource_name):
    query = datastore.query(kind=resource_name)
    for key, value in request.args.items():
        if not value:
            continue
        value = transformer.string2number(value)
        query.add_filter(filter=filters.PropertyFilter(key, "=", value))
    results = list(query.fetch())
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
