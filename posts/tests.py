import itertools
from datetime import datetime
from operator import attrgetter
from unittest.mock import patch

from django.test import TestCase

from posts.models import Post
from posts.tasks import HackerNewsParser, Article, parse_hackernews_site


class HackerNewsParserTests(TestCase):
    @patch.object(HackerNewsParser, 'get_parsed_page')
    @patch.object(HackerNewsParser, 'extract_data')
    def test_parse_skips_duplicates(self, ed, gpp):
        last_articles = [
            'google.com', 'google.ru', 'facebook.com',
        ]
        parsed_articles = [Article(url=url, title='') for url in last_articles + ['facebook.ru']]

        ed.return_value = parsed_articles
        gpp.return_value = object()

        ps = HackerNewsParser()
        new_articles = ps.parse(last_articles)

        self.assertEqual([article.url for article in new_articles], ['facebook.ru'])


class HackerNewsTaskTests(TestCase):
    def setUp(self) -> None:
        Post.objects.create(url='facebook.com', title='facebook', created=datetime.utcnow())

    @patch.object(HackerNewsParser, 'parse')
    def test_parse_hackernews_site_empty_result(self, parse):
        parse.return_value = []

        last_posts = list(Post.objects.all())

        parse_hackernews_site()

        self.assertEqual(list(last_posts), list(Post.objects.all()))

    @patch.object(HackerNewsParser, 'parse')
    def test_parse_hackernews_site_uploads_result(self, parse):
        return_data = [Article(url='google.com', title='google')]
        parse.return_value = return_data

        last_posts = list(Post.objects.all())

        parse_hackernews_site.apply()

        def extract(obj):
            return attrgetter('url', 'title')(obj)

        expected = list(map(extract, itertools.chain(last_posts, return_data)))

        self.assertEqual(expected, list(map(extract, Post.objects.all())))
