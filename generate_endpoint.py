import json

def generate_openapi_schema_multiple(endpoints):
    """
    Generate a JSON schema for OpenAPI documentation (GET operations) for multiple endpoints.

    Args:
        endpoints (list of dict): List of endpoints with name, description, and columns.

    Returns:
        dict: JSON schema for the OpenAPI documentation.
    """
    schema = {
        "openapi": "3.0.0",
        "info": {
            "title": "API Documentation",
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
                        "name": field,
                        "in": "query",
                        "required": False,
                        "schema": {"type": field_type},
                        "description": f"Query parameter for {field}"
                    }
                    for field, field_type in columns.items()
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
                                                    field: {"type": field_type} for field, field_type in columns.items()
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

# Example Usage
endpoints = [
    {
        "endpoint_name": "getUsers",
        "description": "Retrieve a list of users.",
        "columns": {
            "username": "string",
            "email": "string",
            "age": "integer"
        }
    },
    {
        "endpoint_name": "getProducts",
        "description": "Retrieve a list of products.",
        "columns": {
            "productName": "string",
            "price": "number",
            "inStock": "boolean"
        }
    }
]

schema = generate_openapi_schema_multiple(endpoints)
print(json.dumps(schema, indent=4))
