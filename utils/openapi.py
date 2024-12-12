
OPENAPI_DEFINITION_BASE = {
    "openapi": "3.0.0",
    "info": {
        "description": "Auto-generated OpenAPI documentation for your datastore.",
        "version": "1.0.0"
    },
    "paths": {}
}


SWAGGER_UI = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="description" content="SwaggerUI" />
  <title>SwaggerUI</title>
  <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5.11.0/swagger-ui.css" />
</head>
<body>
<div id="swagger-ui"></div>
<script src="https://unpkg.com/swagger-ui-dist@5.11.0/swagger-ui-bundle.js" crossorigin></script>
<script>
  window.onload = () => {
    window.ui = SwaggerUIBundle({
      url: '{{ OPEN_API_URL }}',
      dom_id: '#swagger-ui',
    });
  };
</script>
</body>
</html>
'''


def generate_openapi_definition_from_schema(namespace, datastore_schema):
    openapi_def = dict(OPENAPI_DEFINITION_BASE)
    openapi_def["info"]["title"] = f"Data-API Documentation for `{namespace}` Namespace"
    for kind, properties in datastore_schema.items():
        url = f"/api/{namespace}/{kind}/"
        openapi_def["paths"][url] = {
            "get": {
                "summary": f"List {kind} entities",
                "description": f"Retrieve a list of {kind} entities",
                "parameters": [
                    {
                        "name": property_['name'],
                        "in": "query",
                        "required": False,
                        "schema": {"type": property_['types'][0]},
                        "description": f"Query parameter for {property_['name']}"
                    }
                    for property_ in properties
                ],
                "responses": {
                    "200": {
                        "description": "Successful operation",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "data": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    property_['name']: {"type": property_['types'][0]}
                                                    for property_ in properties
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    return openapi_def
