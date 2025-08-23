import re

import requests
from bs4 import BeautifulSoup, Comment
from markdownify import markdownify as md


def slugify(title):
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


class Scraper:
    def __init__(self, url: str):
        self.url = url

    # fetch article from the API
    def get_articles(self) -> list[dict]:
        response = requests.request("GET", self.url, params={"per_page": 4})
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
    def process_article(self, article: dict) -> None:
        html = self.clean_html(article["body"])
        markdown = md(html, heading_style="ATX")
        title = article["title"]
        slug = slugify(title)
        return {
            "title": title,
            "slug": slug,
            "markdown": f"# {title}\n\n{markdown}",
            "url": article["html_url"],
        }

    def run(self) -> None:
        articles = self.get_articles()
        processed_articles = []
        for article in articles:
            processed_article = self.process_article(article)
            processed_articles.append(processed_article)
        return processed_articles
