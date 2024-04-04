## Buy and Sale of Social Media Profiles
The buying and selling of social media profiles such as Twitter, Instagram, YouTube, and TikTok have been on the rise lately. In this research, we plan to study buying and selling in an end-to-end form.

## Quick Start

Create a `python3` virtual env and install the dependencies:
```
$ python3 -m venv venv
$ venv/bin/pip3 install -r requirements.txt
```

Run a data collection script:
```
$ venv/bin/python3 scripts.FILENAME --conf=$(pwd)/config.yaml
```

where FILENAME is the name of the script you want to run.

## Dependencies

Update using:

```
$ venv/bin/pip3 freeze > requirements.txt
```

## Collaboration Uniformity
For consistency and uniformity, we plan to use selenium as the page-scrapping tool (selenium_driver_util.py) and MongoDB 
as the database (db_util.py) to insert the data collected. The format for insertion into DB will be in the dictionary (or json) 
format for entries. During the scrapping, the automation is expected to scrape each available entry point of the page items.  

```
Example: If you are planning to scrape pages from site "www.z2u.com"

1. First, create a filename z2u_scrape.py, please create a unique filename for each website so that we can all work collaboratively.
2. Identify all the social media platforms for buying and selling (ex. Twitter, Instagram, TikTok, etc.)
3. For each of the social media platforms visit the profiles that are for sale
4. Collect metadata associated with the given profile and insert it in the MongoDB.


example file: z2u_scrape.py

from db_util import MongoDBActor
from selenium_driver_util import PageDriver

class CollectZ2UPageData:
    def __init__(self, social_media): # The idea is to collect social media profiles from each category
        self.social_media = social_media

    def process(self):
        page_driver = PageDriver(URL <- to scrape)
        found_social_media_profiles = [] <-list of pages
        for each_page in found_social_media_profiles:
            entry_data = { ... } <- data associated with the single entry
            MongoDBActor("page_data").insert(entry_data) <- inserts into a collection name "page_data" 

// ----------------------------------------------------------------------------

Page: https://www.z2u.com/items-1822558/-50-FOLLOWERS-TWITTER-ACCOUNTS-VERIFIED-BY-EMAIL-AUTOMATIC-DELIVERY-.html

entry_data = {
  "url": "https://www.z2u.com/items-1822558/-50-FOLLOWERS-TWITTER-ACCOUNTS-VERIFIED-BY-EMAIL-AUTOMATIC-DELIVERY-.html",
  "title": "🔥50 FOLLOWERS - TWITTER ACCOUNTS - VERIFIED BY EMAIL | 🛵🏍️ AUTOMATIC DELIVERY 🛵🏍️",
  "seller": "TalhaAbus",
  "total_order": 10305,
  "rating_pct": "99.5",
  "rating_count": 8739,
  "offer_id": "1822558",
  "pending_offers": 2,
  "description": "If delivery includes ...",
  "price": 0.99,
  "social_media": "twitter"   
}

Note: Not all pages may give the above key, values mentioned, the motive is to collect as much as available
information during data collection.

```

