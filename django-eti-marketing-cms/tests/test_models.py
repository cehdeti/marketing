from django.test import TestCase

import datetime
from django.db import models
from django.utils import timezone
from django.template.defaultfilters import truncatewords

from ckeditor.fields import RichTextField
from django.utils.translation import ugettext as _

import os
from django.conf import settings

from eti_marketing_cms.models import Marketing

class MarketingModelTest(TestCase):

	def setUp(self):
		super(TestCase, self)
		self.__page = Marketing.objects.create(title='Test Title', slug='test-title', columns=Marketing.HALF, page_status='p')

	def test_create_page(self):
		self.assertIsInstance(self.__page, Marketing)

	def test_return_title(self):
		self.assertEqual(str(self.__page), self.__page.title)

	def test_short_title(self):
		self.assertEqual(self.__page.short_title, truncatewords(self.__page.title, 5))

	def test_get_absolute_url(self):
		self.assertEqual(self.__page.get_absolute_url(), "/p/%s/" % self.__page.slug)
