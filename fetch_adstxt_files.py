"""
Fetch ads.txt files from URLs
"""
from datetime import datetime
import logging
import os

import pandas as pd
import requests


logger = logging.getLogger(__name__)


HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
    "Accept": "text/plain"
}


def fetch_adstxt_file(adstxt_url, timeout=5):
    logger.info("fetching ads.txt file from %s", adstxt_url)
    dt = datetime.now()

    try:
        response = requests.get(adstxt_url, headers=HEADERS, timeout=timeout)
        result = {
            "adstxt_url": adstxt_url,
            "failed": False,
            "dt": dt.isoformat(),
            "exception": None,
            "status_code": response.status_code,
            "text": response.text,
        }

    except requests.exceptions.RequestException as oops:
        result = {
            "adstxt_url": adstxt_url,
            "failed": True,
            "dt": dt.isoformat(),
            "exception": repr(oops),
            "status_code": None,
            "text": None,
        }

    return result



if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    all_domains = []

    file_path = "unreliable-news/data/fake-news-codex-2018-06.csv"
    df1 = pd.read_csv(file_path)
    all_domains.extend(df1["domain"].tolist())

    built_with_file = "../data/All-Live-Ads.txt-Sites.csv"
    df_built_with = pd.read_csv(built_with_file, skiprows=1)
    all_domains.extend(df_built_with["Domain"].tolist())

    adstxt_results = []
    for domain in all_domains:
        adstxt_url = "http://{}/ads.txt".format(domain)
        adstxt_fetch_result = fetch_adstxt_file(adstxt_url)
        adstxt_results.append(adstxt_fetch_result)
