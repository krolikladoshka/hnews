from dataclasses import dataclass, asdict
from datetime import datetime
from io import StringIO
from typing import Iterable, List

import requests
from django.db import transaction
from lxml import etree

from hnews.celery import app
from posts.models import Post


@dataclass
class Article:
    url: str
    title: str


class HackerNewsParser:
    base_url = 'https://news.ycombinator.com/'

    def get_parsed_page(self):
        response: requests.Response = requests.get(self.base_url)
        html = response.text

        string_io = StringIO(html)

        parser = etree.HTMLParser()

        return etree.parse(string_io, parser=parser)

    def extract_data(self, page) -> List[Article]:
        return [Article(url=tag.get('href'), title=tag.text)
                for tag in page.xpath("//tr[@class='athing']//td[@class='title']/a")]

    def parse(self, last_articles: Iterable[str]) -> List[Article]:
        last_articles = set(last_articles)

        parsed_page = self.get_parsed_page()
        extracted_articles = self.extract_data(parsed_page)

        return [article for article in extracted_articles if article.url not in last_articles]


@app.task()
def parse_hackernews_site():
    with transaction.atomic():
        last_articles = Post.objects.order_by('-created').values_list('url', flat=True)[:30]

        parser = HackerNewsParser()
        new_articles = parser.parse(last_articles)

        if new_articles:
            posts = [Post(**asdict(article), created=datetime.utcnow()) for article in new_articles]
            Post.objects.bulk_create(posts)
