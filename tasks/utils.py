import concurrent.futures
import logging

import requests
import pandas as pd

logger = logging.getLogger(__name__)


def get_page(api_key: str, page: int = 1) -> list[tuple[str, float]]:
    """Get release_date and vote_average for all movies in a page"""
    url = "https://api.themoviedb.org/3/movie/top_rated"
    params = {"api_key": api_key, "page": page}

    r = requests.get(url, params=params)
    r.raise_for_status()

    results = r.json()["results"]

    # TODO: logger
    print(f"Info: get_page page: {page}, count: {len(results)}")

    return [(item["release_date"], item["vote_average"]) for item in results]


def get_pages(api_key, start, end, max_workers):
    if start < 1 or end > 1000:
        raise ValueError("'start' and 'end' must be between 1 and 1000")

    with concurrent.futures.ThreadPoolExecutor(max_workers) as executor:
        futures_res = [
            executor.submit(get_page, api_key, page) for page in range(start, end + 1)
        ]
        concurrent.futures.wait(futures_res)

    results = [i.result() for i in futures_res]
    flat_result = [item for result in results for item in result]
    return flat_result


def prepare_df(result):
    df = (
        pd.DataFrame(result, columns=["release_date", "vote_average"])
        .assign(year=lambda x: x.release_date.str.split("-", n=1).str.get(0))
        .groupby("year", as_index=False)
        .agg(vote_average=("vote_average", "mean"), quantity=("vote_average", "count"))
    )
    return df


def post_movies(df, api_post_url):
    payload = df.to_json(orient="records")
    headers = {"content-type": "application/json"}
    r = requests.post(api_post_url, data=payload, headers=headers)
    r.raise_for_status()

    return


def scrape_movies(api_key, api_post_url, max_workers=4, max_page=100):
    items = get_pages(api_key, 1, max_page, max_workers)
    df = prepare_df(items)
    post_movies(df, api_post_url)
    logger.info(f"Done scrape_movies, scraped {len(df)} items")
    return "ok"
