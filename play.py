# lets get the files referenced in this medium post
# https://medium.com/@thezedwards/breitbart-com-is-partnering-with-rt-com-other-sites-via-mislabeled-advertising-inventory-6e7e3b5c3318

# https://www.lansingstatejournal.com/story/news/local/2019/10/21/lansing-sun-new-sites-michigan-local-news-outlets/3984689002/
# https://www.nytimes.com/2019/10/21/us/michigan-metric-media-news.html


from collections import defaultdict
from dataclasses import dataclass
import requests
from typing import List


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



def ads_txt_file_from_url(url: str):
    ads_lines = requests.get(url).text.split("\n")
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



urls = [
    "https://www.breitbart.com/ads.txt",
    "https://www.rt.com/ads.txt",
    "https://www.theepochtimes.com/ads.txt",
    "https://www.foxnews.com/ads.txt",
    "https://www.huffpost.com/ads.txt",
    #
    "https://lansingsun.com/ads.txt",

]



atfs = {}
record_to_urls = defaultdict(set)
for url in urls:
    atfs[url] = ads_txt_file_from_url(url)
    for record in atfs[url].records:
        record_to_urls[record].add(url)


print("overlaps")
for record, urls in record_to_urls.items():
    if len(urls) > 1 and record.account_type == "DIRECT":
        print(record, urls)
