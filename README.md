<p align="center">
  <img class="hero-image" src="https://github.com/user-attachments/assets/15d2f888-d0e2-493a-adaf-5338fd6dcf53" alt="logo_and_name" style="width: 100%; max-width: 300px">
</p>

<p align="center">
    <em><strong>Serve Data with Low-Latency</strong></em>
</p>


---

<br>

## 1. Features 🎍 

**`data-api` discovers your datastore data and exposes it as a REST read-only API.**

> 💡 By datastore we mean [firestore in datastore mode](https://cloud.google.com/datastore/docs/concepts/overview).

Features include:

- generates open-api spec definition based on your datastore data
- generates Swagger-UI documentation page based on your datastore data
- expose datastore data via key-value or property-filtering.


<br>

## 2. Deploy 🚀 

Run

```bash
gcloud run deploy data-api \
  --source . \
  --set-env-vars "PROJECT=$PROJECT,DATABASE=$DATABASE"
```

with:

- `$PROJECT` the Google Cloud Project where you datastore database resides
- `$DATABASE` the name of your datastore database (if not given, it will use the default database).

<br>

## Exposed Routes 🚚

Data in datastore is organized in a hierarchy: `database/namespace/kind` (similar to the `database/schema/table` hierarchy in relational databases). 
Inside a `kind` (equivalent to a `table` in relational databases), the `entities` (similar to `rows` in relational database) have a `key` (a string or integer) and a `value` (a dict).

`data-api` Cloud Run service exposes data:

- of the `database` defined as environment variable at deploy time (see above).
- with routes following the datastore organization `/namespace/kind/key`
- following the `metadata` stored in the `_metadata` kind of the `namespace`.

The deployed cloud run service exposes the following routes:

|---------------|-----------------|---------------
| `GET /`       |                 |              |
|---------------|-----------------|---------------

- `GET /` returns a list 
- `GET /docs` returns the specification rendered with Swagger-UI.
- `GET /api/<resource_name>/` returns a list of 100 entities of the kind resource_name.
- `GET /api/<resource_name>/<key>` returns the entity of the kind resource_name that has that key.
- `GET /api/<resource_name>/?foo=bar` returns a list of 100 entities of the kind resource_name where the property/field foo equals bar.

<br>


## 3. Write Data to Datastore ✍️

> We present below:
> 
> 1. how to write data manually to datastore at the expected format
> 2. how you can export a BigQuery table in datastore at expected format with one sql query.



### A. Write data manually to datastore ✍️

1. Open the [Google Cloud Datastore Console](https://console.cloud.google.com/datastore/)
2. Add the schema below as en entity on namespace `[default]` and kind `_schema` (no key required)
3. Add the record below as en entity on namespace `[default]` and kind `customers` with `key` equal to `123`

**Schema**

```json
{
  "kind": "customers",
  "columns": [
    {
      "description": "First name",
      "type": "STRING",
      "name": "first_name"
    },
    {
      "description": "How much money this customer generated for the company",
      "type": "FLOAT64",
      "name": "customer_lifetime_value"
    }
  ]
}
```

**Record**

```json
{
  "first_name": "Paulo",
  "customer_lifetime_value": 8753.35
}
```



### B. Export BigQuery table to datastore ✍️

To export a BigQuery table (data, schema and descriptions)  into `default` namespace of `your-database` in `your-project`, you can run the following query from your BigQuery Console (no install needed):

```sql
call bigfunctions.eu.export_table_to_datastore(
  'your-project.dataset.table',
  'user_id',
  'your-project/your-database/default/users'
);
```

> 💡 If you don't want to pass by public bigfunction, you can deploy the function in your own BigQuery project. You can check the [doc here](https://unytics.io/bigfunctions/bigfunctions/export_table_to_datastore/).




<br>

## 4. GET your Data! 😎

Once you've deployed `data-api` & wrote data to datastore (+ give datastore.user role to cloud run service account) you can GET the documentation and your data on exposed routes:








