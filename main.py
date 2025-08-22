from scrape import Scraper
from upload import Uploader


def main():
    url = "https://support.optisigns.com/api/v2/help_center/en-us/articles"
    scraper = Scraper(url=url)
    scraper.run()
    print("Scraping complete.")

    uploader = Uploader(
        support_dir="support",
        mapping_file="file_mapping.json",
        url_mapping_file="url_mapping.json",
        logs_dir="logs",
    )
    uploader.run()
    print("Upload complete.")


if __name__ == "__main__":
    main()
