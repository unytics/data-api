import os

from flask import Flask, request
import google.cloud.datastore
from google.cloud.datastore import query as filters


import google.auth
creds, project = google.auth.default()

PROJECT = os.environ.get('PROJECT')
print(creds.service_account_email)


app = Flask(__name__)
datastore = google.cloud.datastore.Client(project=PROJECT)


def string2number(string):
    if '.' not in string:
        try:
            return int(string)
        except ValueError:
            pass
    try:
        return float(string)
    except ValueError:
        pass
    return string


@app.route("/")
def hello_world():
    """Example Hello World route."""
    return f"Hello paul!"


@app.route("/<resource_name>/")
def list_records(resource_name):
    query = datastore.query(kind=resource_name)
    for key, value in request.args.items():
        if not value:
            continue
        value = string2number(value)
        query.add_filter(filter=filters.PropertyFilter(key, "=", value))
    results = list(query.fetch())
    return results


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
