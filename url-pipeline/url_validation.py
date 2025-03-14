# validation (run before Scrapy)
import csv
from urllib.parse import urlparse

with open("companies.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        domain = urlparse(row["CareerPortalURL"]).netloc
        assert row["Domain"] == domain, f"Domain mismatch: {row['Domain']} vs {domain}"
