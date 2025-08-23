import json
import os
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup, Comment
from markdownify import markdownify as md


def slugify(title):
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


class Scraper:
    def __init__(
        self,
        url: str,
        output: str = "support",
        url_mapping_file: str = "url_mapping.json",
    ):
        self.url = url
        # check if the output directory exists, if not create it
        self.output = Path(output)
        self.output.mkdir(exist_ok=True)
        self.url_mapping_file = Path(url_mapping_file)
        if os.path.exists(self.url_mapping_file):
            with open(self.url_mapping_file, "r", encoding="utf-8") as f:
                self.url_mapping = json.load(f)
        else:
            self.url_mapping = {}

    # fetch article from the API
    def get_articles(self) -> list[dict]:
        response = requests.request("GET", self.url, params={"per_page": 2})
        if response.status_code == 200:
            data = response.json()
            return data["articles"]
        return []

    def clean_html(self, html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")
        for ul in soup.find_all("ul"):
            if all(
                li.find("a", href=True) and li.find("a")["href"].startswith("#")
                for li in ul.find_all("li")
            ):
                ul.decompose()
        for tag in soup.find_all(["img", "iframe", "script", "video", "style"]):
            tag.decompose()
        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()
        return str(soup)

    # convert the body to md using markdownify library
    def save_article(self, article: dict) -> None:
        html = self.clean_html(article["body"])
        # print(html)
        markdown = md(html, heading_style="ATX")
        title = article["title"]
        slug = slugify(title)
        filename = self.output / f"{slug}.md"
        with open(filename, "w") as f:
            f.write(f"# {title}\n\n")
            f.write(markdown)
        # update url mapping
        self.url_mapping[f"{slug}.md"] = article["html_url"]
        # save mapping JSON
        with open(self.url_mapping_file, "w", encoding="utf-8") as f:
            json.dump(self.url_mapping, f, indent=2)

    def run(self) -> None:
        articles = self.get_articles()
        for article in articles:
            self.save_article(article)


if __name__ == "__main__":
    # https://support.optisigns.com/hc/en-us
    url = "https://support.optisigns.com/api/v2/help_center/en-us/articles"
    Scraper(url).run()
