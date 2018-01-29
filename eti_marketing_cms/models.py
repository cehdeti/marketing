from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError
from django.template.defaultfilters import truncatewords
from django.utils.translation import ugettext as _, ugettext_lazy as __
from django.utils.encoding import python_2_unicode_compatible
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

from ckeditor.fields import RichTextField


class LandingPageQuerySet(models.query.QuerySet):

    def published(self):
        return self.filter(published=True)


@python_2_unicode_compatible
class LandingPage(models.Model):

    LAYOUT_FULL = 'FULL'
    LAYOUT_HALF = 'HALF'
    LAYOUTS = (
        (LAYOUT_FULL, __('Full Width')),
        (LAYOUT_HALF, __('Two Columns')),
    )

    title = models.CharField(__('Page Title'), max_length=200, help_text=__('Try not to exceed 50 characters, long URL or page title is not exactly appealing and it also pushes out of the header block.'))
    slug = models.SlugField(max_length=50, unique=True)

    header = models.BooleanField(__('Header with background image'), default=True, help_text=__('Generic header with a background'))
    subheader = models.CharField(__('Tagline'), max_length=200, help_text=__('This is the article title and should be a bit longer than the page title.'), blank=True)

    seo_keywords = models.CharField(__('Meta Keywords'), max_length=50, blank=True, null=True)
    seo_description = models.CharField(__('Meta Description'), max_length=100, blank=True, null=True)

    # Layouts
    columns = models.CharField(max_length=4, choices=LAYOUTS, default=LAYOUT_FULL)
    sidebar = models.BooleanField(__('Sidebar?'), default=False)
    column_1 = RichTextField(help_text=__('This is left content box'))
    column_2 = RichTextField(help_text=__('You don\'t have to fill this in if you have only one column'), blank=True, null=True)
    sidebar_text = RichTextField(help_text=__('Sidebar Text if <b>Sidebar</b> is turned on'), blank=True, null=True)

    cta = models.BooleanField(__('Call to Action Button?'), default=True)
    cta_text = models.CharField(__('Button Text'), max_length=30, blank=True, null=True, default='Contact Us', help_text=__('Default is: Contact Us'))
    cta_url = models.CharField(__('Button URL'), max_length=300, blank=True, null=True, default='/contact/', help_text=__('Within our site: /contact/. External Site: https://google.com/'))

    footer = models.BooleanField(__('Show Footer?'), default=True)

    # Social media
    socials = models.BooleanField(__('Share Article on Social Media?'), default=False, help_text=__('You have to customize this on your AddThis account'))
    addthis_pubid = models.CharField(__('AddThis PubId'), max_length=25, null=True, blank=True, help_text=__('This is the string that is AFTER `#pubid=`. Ex: ra-5a61fe428f3a39a8'))

    # Article publishing
    added_date = models.DateTimeField(__('Date Added'), auto_now_add=True)
    last_updated = models.DateTimeField(__('Last Update'), auto_now=True)
    published = models.BooleanField(__('Publish Page?'), default=False, help_text=__('Unpublished pages are only visible to admins.'))

    objects = LandingPageQuerySet.as_manager()

    def clean(self):
        if self.socials and not self.addthis_pubid:
            raise ValidationError(_('AddThis PubId is required'))

    @property
    def short_title(self):
        return truncatewords(self.title, 5)

    def get_absolute_url(self):
        return reverse('marketing-landing-page', args=[self.slug])

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = __('Landing Page')
        verbose_name_plural = __('Landing Pages')
        ordering = ('title',)
