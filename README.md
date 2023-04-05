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
git clone https://github.com/lbellomo/movie_review.git
cd movie_review

# copy .env template and complete the themoviedb.org API_KEY
# (you can get one at https://developers.themoviedb.org/3 ),
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

## Development setup

### Install dependencies

Create a new virtual env with `python3.11`, activate it and install dependencies (only needed for IDE autocompletion and running tools like linters in development). I use [mambaforge](https://github.com/conda-forge/miniforge#mambaforge) but anything will do.

```
mamba create -n movie_review python=3.11
mamba activate movie_review

pip install -r requirements-dev.txt
pip install -r app/requirements.txt
pip install -r tasks/requirements.txt
```

### Run linters

```
# in the project home
black
flake8 --max-line-length 88
```

### Pin dependencies

To create the `requirements.txt` with dependencies pinned from `requirements.in`

```
pip-compile --output-file=- > requirements.txt
# or 
pip-compile --output-file=- requirements-dev.in > requirements-dev.txt
```
