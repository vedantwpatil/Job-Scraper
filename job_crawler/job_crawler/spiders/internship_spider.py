import os
import csv
import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from urllib.parse import urlparse


class InternshipSpider(CrawlSpider):
    name = "internship_spider"

    # Terms we're looking for in job titles or descriptions
    CS_TERMS = [
        "computer science",
        "software",
        "developer",
        "engineer",
        "programming",
        "data science",
        "machine learning",
        "ai",
        "artificial intelligence",
        "web developer",
        "full stack",
        "frontend",
        "backend",
        "devops",
        "cloud",
        "coding",
        "coder",
        "python",
        "java",
        "javascript",
        "c++",
        "algorithms",
    ]

    INTERNSHIP_TERMS = [
        "intern",
        "internship",
        "co-op",
        "coop",
        "student",
        "summer",
        "undergraduate",
        "graduate",
        "university",
    ]

    def __init__(self, *args, **kwargs):
        super(InternshipSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = []
        self.start_urls = []
        self.company_map = {}  # Map URLs to company names

        # Read from the CSV file
        file_path = "/Users/vedantpatil/OneDrive - Drexel University/Documents/CS/personal/projects/python/web/webscraping/job-applications/url-pipeline/urls-to-crawl-cleaned.csv"

        with open(file_path, "r") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if len(row) >= 3:
                    company_name, domain, careers_url = row

                    # Clean domain (remove any protocols and www)
                    parsed = urlparse(domain)
                    clean_domain = parsed.netloc or parsed.path
                    clean_domain = clean_domain.replace("www.", "")

                    # Add to allowed domains
                    self.allowed_domains.append(clean_domain)

                    # Add to start URLs
                    self.start_urls.append(careers_url)

                    # Map this URL to company name
                    self.company_map[careers_url] = company_name

        print(f"Loaded {len(self.allowed_domains)} companies to crawl")

    # Define rules for following links
    rules = (
        # Follow links that look like job listings
        Rule(
            LinkExtractor(
                allow=(
                    "job",
                    "career",
                    "position",
                    "opening",
                    "listing",
                    "intern",
                    "opportunity",
                )
            ),
            callback="parse_item",
            follow=True,
        ),
        # Also follow general links on career pages, but don't process them
        Rule(LinkExtractor(), follow=True),
    )

    def parse_item(self, response):
        """Process a page that might contain job listings"""
        # Extract all text from the page
        page_text = " ".join(response.xpath("//body//text()").getall()).lower()

        # Check if this page talks about internships and CS
        is_internship = any(term in page_text for term in self.INTERNSHIP_TERMS)
        is_cs = any(term in page_text for term in self.CS_TERMS)

        # If this looks like a CS internship, extract details
        if is_internship and is_cs:
            # Try to extract job title - different sites structure this differently
            job_title = self.extract_job_title(response)

            # Get the company name from our map, or try to extract it
            company_name = self.get_company_name(response)

            # Try to get location
            location = self.extract_location(response, page_text)

            # Get application URL
            apply_url = self.extract_apply_url(response)

            # Yield the result
            yield {
                "company": company_name,
                "title": job_title,
                "location": location,
                "url": response.url,
                "apply_url": apply_url,
                "source": "career site",
            }

    def extract_job_title(self, response):
        """Try various selectors to find job title"""
        # Common selectors for job titles
        selectors = [
            "//h1",
            "//h2",
            "//title",
            '//meta[@property="og:title"]/@content',
            '//div[contains(@class, "job-title")]',
            '//div[contains(@class, "position-title")]',
            '//span[contains(@class, "job-title")]',
        ]

        for selector in selectors:
            title = response.xpath(selector).get()
            if title:
                title = title.strip()
                # Check if title contains relevant keywords
                if any(term in title.lower() for term in self.INTERNSHIP_TERMS) and any(
                    term in title.lower() for term in self.CS_TERMS
                ):
                    return title

        return "Unknown Title"

    def get_company_name(self, response):
        """Get company name from our mapping or try to extract it"""
        # First check our map
        for start_url, company in self.company_map.items():
            if start_url in response.url:
                return company

        # Otherwise try to extract from page
        selectors = [
            '//meta[@property="og:site_name"]/@content',
            '//meta[@name="author"]/@content',
            "//title",
        ]

        for selector in selectors:
            name = response.xpath(selector).get()
            if name:
                return name.strip().split("|")[0].strip()

        # Fallback to domain
        domain = urlparse(response.url).netloc
        return domain.replace("www.", "").split(".")[0].capitalize()

    def extract_location(self, response, text):
        """Try to find job location"""
        # Look for common location patterns
        location_patterns = [
            r"location:?\s*([^,\.;]+(?:,[^,\.;]+)?)",
            r"position located in:?\s*([^,\.;]+(?:,[^,\.;]+)?)",
            r"remote|onsite|hybrid|in-person",
        ]

        for pattern in location_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return (
                    match.group(1).strip() if match.groups() else match.group(0).strip()
                )

        return "Unknown Location"

    def extract_apply_url(self, response):
        """Find application URL"""
        # Look for apply buttons
        apply_links = response.xpath(
            '//a[contains(@href, "apply") or contains(text(), "Apply") or contains(@class, "apply")]/@href'
        ).getall()

        if apply_links:
            apply_url = response.urljoin(apply_links[0])
            return apply_url

        return response.url  # Default to current page if no apply link found
