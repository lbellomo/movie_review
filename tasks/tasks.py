import os
import logging

from celery import Celery
from celery.schedules import crontab

from utils import scrape_movies

BROKER_URL = os.environ["BROKER_URL"]
API_KEY = os.environ["API_KEY"]
API_POST_URL = os.environ["API_POST_URL"]
MAX_WORKERS = int(os.environ["MAX_WORKERS"])
MAX_PAGE = int(os.environ["MAX_PAGE"])

logger = logging.getLogger(__name__)

app = Celery("tasks", broker=BROKER_URL)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute="*/30"),
        scrape.s(API_KEY, API_POST_URL, MAX_WORKERS, MAX_PAGE),
        name="scrape films every 30 min",
    )


@app.task
def scrape(api_key, api_post_url, max_workers, max_page):
    scrape_movies(api_key, api_post_url, max_workers, max_page)
