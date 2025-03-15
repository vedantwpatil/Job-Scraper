import scrapy
import csv


class InternshipSpider(scrapy.Spider):
    name = "internship_scraper"

    def __init__(self):
        file_path = "../../../url-pipeline/urls-to-crawl.csv"

        with open(file_path) as f:
            data = csv.DictReader(f)
            self.allowed_domains = [row["Domain"] for row in data]

            f.seek(0)  # Reset file pointer
            self.start_urls = [row["CareerPortalURL"] for row in data]

    def parse(self, response):
        pass
