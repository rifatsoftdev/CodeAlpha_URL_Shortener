# URL Shortener

A lightweight URL shortener built with FastAPI, SQLAlchemy, and SQLite. Create shareable short links, redirect visitors to their original URLs, and track clicks. Short links expire after 14 days.

## Features

- Validates submitted URLs as HTTP or HTTPS links.
- Generates a unique short code for each link.
- Redirects short links to their original destinations.
- Tracks the number of times a short link is used.
- Removes expired links and shows a custom 404 page for missing or expired links.
- Includes a browser-based page for shortening links.

## Requirements

- Docker Engine or Docker Desktop

Python and pip are not required on the host machine; the application runs in a Docker container.

## Run with Docker

Build the image from the project directory:

```bash
docker build -t url-shortener .
```

Start the container:

```bash
docker run -d \
  --name url-shortener \
  -p 8000:8000 \
  --mount type=bind,source="$(pwd)/database.db",target=/app/database.db \
  url-shortener
```

The named Docker volume `url-shortener-data` keeps the SQLite database when the container is removed or recreated. To start the existing container again, use `docker start url-shortener`.

Open [http://localhost:8000](http://localhost:8000) to use the web interface. Interactive API documentation is available at [http://localhost:8000/docs](http://localhost:8000/docs).

To stop and remove the container:

```bash
docker stop url-shortener
docker rm url-shortener
```

The database volume remains after removing the container. To permanently delete the stored database, remove the volume:

```bash
docker volume rm url-shortener-data
```

## API

### Create a short URL

`POST /add-new-url`

Request body:

```json
{
  "url": "https://example.com/a/long/page"
}
```

Example response:

```json
{
  "short_url": "http://localhost:8000/AbCdEf12"
}
```

The response contains the absolute short URL for the host used in the request. Invalid or non-HTTP(S) URLs are rejected with HTTP `422`.

### Follow a short URL

`GET /{short_code}`

For example, `GET /AbCdEf12` redirects to the original URL and increments its click count. If the code does not exist or has expired, the server displays the custom 404 page and returns HTTP `404`.

## Storage and expiration

The app uses the SQLite database file `database.db` inside the container. The Docker volume mounted at `/app/database.db` persists the database across container restarts and replacements. The `urls` table stores original URLs, short codes, click counts, creation timestamps, and expiration timestamps. Expired records are removed when a new short URL is created or when an expired short link is requested.

## Project structure

```text
Dockerfile       Builds the application image
app/
  database.py    SQLAlchemy engine, session setup, and database dependency
  main.py        FastAPI application and routes
  models.py      URL database model
  schema.py      Request validation schema
static/
  index.html     URL-shortening web interface
  404.html       Missing/expired short-link page
requirements.txt Python dependencies installed in the image
```
