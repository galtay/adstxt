# lets get the files referenced in this medium post
# https://medium.com/@thezedwards/breitbart-com-is-partnering-with-rt-com-other-sites-via-mislabeled-advertising-inventory-6e7e3b5c3318

# https://www.lansingstatejournal.com/story/news/local/2019/10/21/lansing-sun-new-sites-michigan-local-news-outlets/3984689002/
# https://www.nytimes.com/2019/10/21/us/michigan-metric-media-news.html

# TODO: handle 403 codes for the default python requests user agent [done]
# TODO: add host url and datetime scraped info to AdsTxtRecord or AdsTxtFile
# TODO: handle ads.txt urls that redirect to html pages ...
#    easy hack: ratio of good adstxt lines to malformed lines?
#    better hack: detect if page is html and skip?


from collections import defaultdict
from dataclasses import dataclass
from typing import List

import pandas as pd
import requests


HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"}


@dataclass(frozen=True)
class AdsTxtRecord:
    ad_system_domain: str
    pub_account_id: str
    account_type: str
    cert_auth_id: str=None


@dataclass(frozen=True)
class AdsTxtFile:
    url: str
    records: List[AdsTxtRecord]

    def __iter__(self):
        for record in self.records:
            yield record



def ads_txt_file_from_url(url: str):
    try:
        res = requests.get(url, headers=HEADERS)
        print(res.status_code)
    except requests.exceptions.RequestException as oops:
        return AdsTxtFile(url, [])
    if not res.ok:
        return AdsTxtFile(url, [])

    ads_lines = res.text.split("\n")
    ads_records = []
    for line in ads_lines:
        line = line.strip()
        if line.startswith("#"):
            continue
        while "#" in line:
            line = line[:line.rfind("#")].strip()
        if line == "":
            continue

        try:
            atl = AdsTxtRecord(*[el.strip() for el in line.split(",")])
            ads_records.append(atl)
        except:
            print("MALFORMED: ", line)

    return AdsTxtFile(url, ads_records)



df1 = pd.read_csv("unreliable-news/data/buzzfeed-2018-12.csv")
urls1 = ['http://www.{}/ads.txt'.format(val) for val in df1['domain'].values]
#df2 =


urls = [
    "https://www.breitbart.com/ads.txt",
    "https://www.rt.com/ads.txt",
    "https://www.theepochtimes.com/ads.txt",
    "https://www.foxnews.com/ads.txt",
    "https://www.huffpost.com/ads.txt",
    #
    "https://lansingsun.com/ads.txt",

] + urls1



atfs = {}
record_to_urls = defaultdict(set)
for url in urls:
    print(url)
    atf = ads_txt_file_from_url(url)
    atfs[url] = ads_txt_file_from_url(url)
    for record in atfs[url].records:
        record_to_urls[record].add(url)


print("overlaps")
for record, urls in record_to_urls.items():
    if len(urls) > 1 and record.account_type == "DIRECT":
        print(record, urls)
