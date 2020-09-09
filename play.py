# lets get the files referenced in this medium post
# https://medium.com/@thezedwards/breitbart-com-is-partnering-with-rt-com-other-sites-via-mislabeled-advertising-inventory-6e7e3b5c3318


from dataclasses import dataclass
import requests
from typing import List


@dataclass(frozen=True)
class AdsTxtRecord:
    ad_system_domain: str
    pub_account_id: str
    account_type: str
    ceert_auth_id: str=None


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
#            sys.exit(1)

    return AdsTxtFile(url, ads_records)





url = "https://www.breitbart.com/ads.txt"
breitbart_atf = ads_txt_file_from_url(url)

url = "https://www.rt.com/ads.txt"
rt_atf = ads_txt_file_from_url(url)



intersection = set(breitbart_atf.records) & set(rt_atf.records)
direct_intersect = [
    record for record in intersection if record.account_type == "DIRECT"]

print()
print("direct records from both sites: ")
for record in direct_intersect:
    print(record)
