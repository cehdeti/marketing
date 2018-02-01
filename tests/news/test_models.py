from django.test import TestCase
from django.template.defaultfilters import truncatewords
from eti_marketing.news.models import Article


class ArticleTest(TestCase):

    def setUp(self):
        super().setUp()
        self.__article = Article.objects.create(
            title='Test Title',
            slug='test-title',
            columns=Article.LAYOUT_HALF,
            published=True
        )

    def test_str(self):
        self.assertEqual(str(self.__article), self.__article.title)

    def test_short_title(self):
        self.assertEqual(self.__article.short_title, truncatewords('Test Title', 5))

    def test_get_absolute_url(self):
        self.assertEqual(self.__article.get_absolute_url(), '/news/test-title/')
