<p align="center">
  <img class="hero-image" src="https://github.com/user-attachments/assets/15d2f888-d0e2-493a-adaf-5338fd6dcf53" alt="logo_and_name" style="width: 100%; max-width: 300px">
</p>

<p align="center">
    <em><strong>Serve Data with Low-Latency</strong></em>
</p>


---

<br>

## 1. Features 🎍

**`data-api` discovers your datastore data & exposes them as a REST read-only API.**

> 💡 By datastore we mean [firestore in datastore mode](https://cloud.google.com/datastore/docs/concepts/overview).

Features include:

- generate open-api spec definition
- generate Swagger-UI documentation page
- expose datastore data via key-value or property-filtering.
- cache responses with configurable duration
- manage permissions with api-keys or openID tokens.

> 💡 `data-api` is great to create a low-latency API for your **BigQuery** data
> (that you can export to datastore with one sql query. More below).


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

## 3. Exposed Routes 🚚

> 💡 **Datastore Reminder**:
>
> - Data in datastore is organized in a hierarchy: `database/namespace/kind` (like the `database/schema/table` hierarchy in relational databases).
> - Inside a `kind` (think `table`), the `entities` (think `rows`) have a `key` (a string or integer) and a `value` (a dict).

<br>

`data-api` Cloud Run service:

- exposes the data of the `database` defined as environment variable at deploy time (see above).
- considers each `namespace` as a different api (which has its own open-api spec definition and Swagger UI).
- exposes the following routes (with `GET` method):

| url                                | Description                                                                                      |
|------------------------------------|--------------------------------------------------------------------------------------            |
| `/`                                | Redirects to `/api/`                                                                             |
| `/api/`                            | Returns the list of namespaces in `database`                                                     |
| `/api/<namespace>/`                | Returns details on `namespace` api including its `kinds` and urls                                |
| `/api/<namespace>/openapi.json`    | Returns the openapi spec definition of the `namespace` api                                       |
| `/api/<namespace>/swagger-ui.html` | Returns the Swagger UI (documentation portal) of the `namespace` api                             |
| `/api/<namespace>/<kind>/`         | Returns a list of entity values of `kind`                                                        |
| `/api/<namespace>/<kind>/<key>`    | Returns the entity value of `key`                                                                |
| `/api/<namespace>/<kind>/?foo=bar` | Returns a list of entity values of `kind` for which `foo` property is equal to `bar`             |

<br>



## 4. Export BigQuery table to datastore ✍️

To export a BigQuery table into `default` namespace of `your-database` in `your-project`, you can run the following query from your BigQuery Console (no install needed):

```sql
call bigfunctions.eu.export_table_to_datastore(
  'your-project.dataset.table',
  'user_id',
  'your-project/your-database/default/users'
);
```

> 💡 If you don't want to pass by the public bigfunction, you can deploy the function in your own BigQuery project. Check the [function documentation](https://unytics.io/bigfunctions/bigfunctions/export_table_to_datastore/).




<br>

## 5. GET your Data! 😎

Once you've deployed `data-api` & wrote data to datastore (+ give datastore.user role to cloud run service account) you can GET the documentation and your data on exposed routes:
