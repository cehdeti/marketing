from django.test import TestCase
from django.template.defaultfilters import truncatewords
from eti_marketing.landing_page.models import LandingPage


class LandingPageTest(TestCase):

    def setUp(self):
        super().setUp()
        self.__page = LandingPage.objects.create(
            title='Test Title',
            slug='test-title',
            columns=LandingPage.LAYOUT_HALF,
            published=True
        )

    def test_str(self):
        self.assertEqual(str(self.__page), self.__page.title)

    def test_short_title(self):
        self.assertEqual(self.__page.short_title, truncatewords('Test Title', 5))

    def test_get_absolute_url(self):
        self.assertEqual(self.__page.get_absolute_url(), '/p/test-title/')
