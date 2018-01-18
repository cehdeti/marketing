from __future__ import unicode_literals
import datetime


from django.db import models
from django.utils import timezone
from django.template.defaultfilters import truncatewords

from ckeditor.fields import RichTextField
from django.utils.translation import ugettext as _

import os
from django.conf import settings

class Marketing(models.Model):

  LAYOUT_FULL = 'FULL'
  LAYOUT_HALF = 'HALF'
  LAYOUTS = (
    (LAYOUT_FULL, 'Full Width'),
    (LAYOUT_HALF, 'Two Columns')
  )

  title = models.CharField(_('Page Title'), max_length=200, help_text=_('Try not to exceed more than 50 characters, long URL or page title is not exactly appealing and it also pushes out of the header block.'))
  slug = models.SlugField(max_length=50, unique=True)
  header = models.BooleanField(_('Header with background image'), default=True, help_text=_("Generic header with a background"))
  header_bg = models.FilePathField(_("Header Background Image"), path=settings.MARKETING_IMGF_FILEPATH, blank=True, null=True)
  subheader = models.CharField(_("Tagline"), max_length=200, help_text=_("This is the article title and should be a bit longer than the page title."), blank=True)
  seo_keywords = models.CharField(_('Meta Keywords'), max_length=50, blank=True, null=True)
  seo_description = models.CharField(_('Meta Description'), max_length=100, blank=True, null=True)
  columns = models.CharField(max_length=4, choices=LAYOUTS, default=LAYOUT_FULL)
  sidebar = models.BooleanField(_('Turn sidebar on?'), default=False)
  column_1 = RichTextField(help_text=_("This is left content box"), blank=False, null=False)
  column_2 = RichTextField(help_text=_("You don't have to fill this in if you have only one column"), blank=True)
  sidebar_text = RichTextField(help_text=_("Sidebar Text if <b>Sidebar</b> is turned on"), blank=True)
  cta = models.BooleanField(_('Call to Action Button?'), default=True)
  cta_text = models.CharField(_('Button Text'), max_length=30, blank=True, null=True, default="Contact Us", help_text=_('Default is: Contact Us'))
  cta_url = models.CharField(_('Button URL'), max_length=300, blank=True, null=True, default="/contact/", help_text=_('Within our site: /contact/. External Site: https://google.com/'))
  footer = models.BooleanField(_('Show Footer?'), default=True)
  socials = models.BooleanField(_('Social Icons?'), default=False)
  added_date = models.DateTimeField(_('Date Added'), auto_now_add=True)
  last_updated = models.DateTimeField(_('Last Update'), auto_now=True)
  published = models.BooleanField(_('Publish Page?'), default=False, help_text=_("Make sure you set the page status to Publish, otherwise it is hidden."))

  def __str__(self):
    return self.title

  @property
  def short_title(self):
    return truncatewords(self.title, 5)

  def get_absolute_url(self):
    return "/p/%s/" % (self.slug)