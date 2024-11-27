SWAGGER_TEMPLATE = {
    "swagger": "2.0",
    "info": {
        "title": "DataAPI Documentation",
        "description": "Auto-generated API documentation with Swagger UI.",
        "version": "1.0.0"
    },
    "paths": {}
}


SWAGGER_CONF = {
        "headers": [
        ],
        "specs": [
            {
                "endpoint": 'swagger',
                "route": '/swagger.json',
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
            }
        ],
        "static_url_path": "/flasgger_static",
        # "static_folder": "static",  # must be set by user
        "swagger_ui": True,
        "specs_route": "/docs/"
    }
