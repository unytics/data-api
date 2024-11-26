<p align="center">
  <img class="hero-image" src="https://github.com/user-attachments/assets/15d2f888-d0e2-493a-adaf-5338fd6dcf53" alt="logo_and_name" style="width: 100%; max-width: 600px">
</p>

<p align="center">
    Serve Data with Low-Latency
</p>


---

<br>



## Routes

- `GET /` returns the OpenAPI specification generated on-the-fly from schemas stored in Datastore.
- `GET /docs` returns the specification rendered with Swagger-UI.
- `GET /<resource_name>/` returns a list of 100 entities of the kind resource_name.
- `GET /<resource_name>/<key>` returns the entity of the kind resource_name that has that key.
- `GET /<resource_name>/foo=bar` returns a list of 100 entities of the kind resource_name where the property/field foo equals bar.

## Deploy

Run

```
gcloud run deploy data-api --source . --set-env-vars "PROJECT=$PROJECT"
```
