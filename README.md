<p align="center">
  <img class="hero-image" src="https://github.com/user-attachments/assets/15d2f888-d0e2-493a-adaf-5338fd6dcf53" alt="logo_and_name" style="width: 100%; max-width: 600px">
</p>

<p align="center">
    <em><strong>Serve Data with Low-Latency</strong></em>
</p>


---

<br>

## Features

`data-api` discovers your datastore data and exposes it as a REST read-only API (*datastore = "firestore in datastore mode"*)

Features include:

- generates open-api spec definition based on your datastore data
- generates Swagger-UI documentation page based on your datastore data
- expose datastore data via key-value or property-filtering.


<br>

## Deploy

Run

```bash
gcloud run deploy data-api \
  --source . \
  --set-env-vars "PROJECT=$PROJECT,DATABASE=$DATABASE"
```

with:

- `$PROJECT` the Google Cloud Project where you datastore database resides
- `$DATABASE` the name of your datastore database (if not given, it will check on default database).

<br>

## Write Data to Datastore 

### 1. Export BigQuery table to datastore for automatic discovery by data-api

To export a BigQuery table (data & schema)  into `default` namespace of `your-database` in `your-project`, you can run the following query from your BigQuery Console (no install needed):

```sql
call bigfunctions.eu.export_table_to_datastore(
  'your-project.dataset.table',
  'user_id',
  'your-project/your-database/default/users'
);
```

> 💡 If you don't want to pass by public bigfunction, you can deploy the function in your own BigQuery project. You can check the [doc here](https://unytics.io/bigfunctions/bigfunctions/export_table_to_datastore/).

<br>


### 2. Write data directly

1. Open the [Google Cloud Datastore Console](https://console.cloud.google.com/datastore/)
2. Add the schema below as en entity on namespace `[default]` and kind `_schema` (no key required)
3. Add the record below as en entity on namespace `[default]` and kind `customers` with `key` equal to `1`

**schema**: 

```json
{
  "columns": [
    {
      "description": "",
      "type": "STRING",
      "name": "customer_id"
    },
    {
      "description": "",
      "type": "STRING",
      "name": "first_name"
    },
    {
      "description": "",
      "type": "FLOAT64",
      "name": "customer_lifetime_value"
    }
  ],
  "kind": "customers"
}
```

**record**

```json
```



<br>

## Exposed Routes



- `GET /` returns the OpenAPI specification generated on-the-fly from schemas stored in Datastore.
- `GET /docs` returns the specification rendered with Swagger-UI.
- `GET /api/<resource_name>/` returns a list of 100 entities of the kind resource_name.
- `GET /api/<resource_name>/<key>` returns the entity of the kind resource_name that has that key.
- `GET /api/<resource_name>/?foo=bar` returns a list of 100 entities of the kind resource_name where the property/field foo equals bar.

<br>



