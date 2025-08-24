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


if __name__ == "__main__":
    main()
