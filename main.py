import time

import schedule

from scrape import Scraper
from upload import Uploader


def main():
    url = "https://support.optisigns.com/api/v2/help_center/en-us/articles"
    scraper = Scraper(url=url)
    articles = scraper.run()
    print("Scraping complete.")

    uploader = Uploader()
    uploader.run(articles)
    print("Upload complete.")


schedule.every(5).minutes.do(main)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(60)
