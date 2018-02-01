from django.db import models
from django.template.defaultfilters import truncatewords
from django.utils.translation import ugettext as _, ugettext_lazy as __
from django.utils.encoding import python_2_unicode_compatible
from django.core.exceptions import ValidationError
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

from ckeditor.fields import RichTextField


class ArticleQuerySet(models.query.QuerySet):

    def published(self):
        return self.filter(published=True)


@python_2_unicode_compatible
class Article(models.Model):

    LAYOUT_FULL = 'FULL'
    LAYOUT_HALF = 'HALF'
    LAYOUTS = (
        (LAYOUT_FULL, __('Full Width')),
        (LAYOUT_HALF, __('Two Columns')),
    )

    title = models.CharField(__('Page Title'), max_length=200, help_text=__('Try not to exceed more than 50 characters (for aesthetic reasons).'))
    slug = models.SlugField(max_length=50, unique=True)
    header = models.BooleanField(__('Header with background image'), default=True, help_text=__('Generic header with a background'))
    subheader = models.CharField(__('Tagline'), max_length=200, help_text=__('This is the article title and should be a bit longer than the page title.'), blank=True)
    seo_keywords = models.CharField(__('Meta Keywords'), max_length=50, blank=True, null=True)
    seo_description = models.CharField(__('Meta Description'), max_length=100, blank=True, null=True)
    columns = models.CharField(max_length=4, choices=LAYOUTS, default=LAYOUT_FULL)
    sidebar = models.BooleanField(__('Turn sidebar on?'), default=False)
    column_1 = RichTextField(help_text=__('This is left content box'))
    column_2 = RichTextField(help_text=__('You don\'t have to fill this in if you have only one column'), blank=True)
    sidebar_text = RichTextField(help_text=__('Sidebar Text if <b>Sidebar</b> is turned on'), blank=True)
    cta = models.BooleanField(__('Call to Action Button?'), default=True)
    cta_text = models.CharField(__('Button Text'), max_length=30, blank=True, null=True, default='More News Articles', help_text=__('Default is: More News Articles'))
    cta_url = models.CharField(__('Button URL'), max_length=300, blank=True, null=True, default="/news/", help_text=_('Within our site: /news/. External Site: https://google.com/'))
    footer = models.BooleanField(__('Show Footer?'), default=True)
    socials = models.BooleanField(__('Social Icons?'), default=False)
    addthis_pubid = models.CharField(__('AddThis PubId'), max_length=25, null=True, blank=True, help_text=__('This is the string that is AFTER `#pubid=`. Ex: ra-5a61fe428f3a39a8'))
    added_date = models.DateTimeField(__('Date Added'), auto_now_add=True)
    last_updated = models.DateTimeField(__('Last Update'), auto_now=True)
    published = models.BooleanField(__('Publish Page?'), default=False, help_text=__('Unpublished pages are only visible to admins.'))

    objects = ArticleQuerySet.as_manager()

    @property
    def short_title(self):
        return truncatewords(self.title, 5)

    def get_absolute_url(self):
        return reverse('news-article-detail', args=[self.slug])

    def clean(self):
        if self.socials and not self.addthis_pubid:
            raise ValidationError(_('AddThis PubId is required'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = __('News Article')
        verbose_name_plural = __('News Articles')
