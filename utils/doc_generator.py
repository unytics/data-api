import json

def generate_openapi_schema(endpoints):

    schema = {
        "openapi": "3.0.0",
        "info": {
            "title": "DataAPI Documentation",
            "description": "Auto-generated OpenAPI documentation for multiple endpoints.",
            "version": "1.0.0"
        },
        "paths": {}
    }

    for endpoint in endpoints:
        endpoint_name = endpoint["endpoint_name"]
        description = endpoint["description"]
        columns = endpoint["columns"]

        # Add the endpoint to paths
        schema["paths"][f"/{endpoint_name}"] = {
            "get": {
                "summary": description,
                "parameters": [
                    {
                        "name": field.get('name'),
                        "in": "query",
                        "required": False,
                        "schema": {"type": field.get('type')},
                        "description": field.get('description', f"Query parameter for {field.get('name')}")
                    }
                    for field in columns
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
                                                    field.get('name'): {"type": field.get('type')} for field in columns
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

    return schema
