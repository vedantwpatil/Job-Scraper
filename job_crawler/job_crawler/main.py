import os
import argparse
from job_crawler.job_crawler.spiders import internship_spider
from spiders.internship_spider import InternshipSpider
from analyze_results import analyze_results


def main():
    parser = argparse.ArgumentParser(description="Scrape CS internship postings")
    parser.add_argument(
        "--skip-crawl",
        action="store_true",
        help="Skip crawling and just analyze existing results",
    )
    args = parser.parse_args()

    if not args.skip_crawl:
        print("Starting crawler to find CS internships...")
        internship_spider.run_spider()

    print("Analyzing results...")
    analyze_results()

    print("\nDone!")


if __name__ == "__main__":
    main()
