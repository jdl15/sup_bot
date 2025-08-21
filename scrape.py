import re
from pathlib import Path

import requests
from markdownify import markdownify as md


def slugify(title):
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


class Scraper:
    def __init__(self, url: str, output: str = "support"):
        self.url = url
        # check if the output directory exists, if not create it
        self.output = Path(output)
        self.output.mkdir(exist_ok=True)

    # fetch article from the API
    def get_articles(self) -> list[dict]:
        response = requests.request("GET", self.url)
        # data key: dict_keys(['count', 'next_page', 'page', 'page_count', 'per_page',
        # 'previous_page', 'articles', 'sort_by', 'sort_order'])
        if response.status_code == 200:
            data = response.json()
            return data["articles"]
        return []

    # convert the body to md using markdownify library
    # article key: dict_keys(['id', 'url', 'html_url', 'author_id', 'comments_disabled', 'draft', 'promoted', 'position',
    # 'vote_sum', 'vote_count', 'section_id', 'created_at', 'updated_at', 'name', 'title', 'source_locale', 'locale',
    # 'outdated', 'outdated_locales', 'edited_at', 'user_segment_id', 'permission_group_id', 'content_tag_ids', 'label_names', 'body'])
    def save_article(self, article: dict) -> None:
        html = article["body"]
        markdown = md(html, heading_style="ATX")
        title = article["title"]
        slug = slugify(title)
        filename = self.output / f"{slug}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n")
            f.write(markdown)

    def run(self) -> None:
        articles = self.get_articles()
        for article in articles:
            self.save_article(article)


if __name__ == "__main__":
    # https://support.optisigns.com/hc/en-us
    url = "https://support.optisigns.com/api/v2/help_center/en-us/articles"
    Scraper(url).run()
