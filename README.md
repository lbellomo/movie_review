# Movie Review

Simple scraper for `themoviedb.org` api.

## Overview

The project mainly consists of two images:
- `celery` (in the `task/` dir) that downloads the top movies from the foo api every 30 minutes and posts the results by aggregates per year to the local api when finished.
- `api` (in the `app/` dir) with two endpoints `GET /v1/movies` to check the movies that are saved in the db and `POST /v1/movies` to save in the db.

It also uses two more images: `rabbitmq` for the celery and `postgres` for the api.

## Setup

Make sure you have a modern version of docker installed.

```
git clone 
cd movie_review

# copy .env template and complete the API_KEY,
# POSTGRES_PASSWORD and SQLALCHEMY_DATABASE_URI
# You can also change the concurrency and the number of scraped pages.
cp .env.sample .env
nano .env

# build imgs 
docker compose build
# run migrations on db (only once)
docker compose run --rm api bash -c 'alembic upgrade head'
# start all containers
docker compose up
```
