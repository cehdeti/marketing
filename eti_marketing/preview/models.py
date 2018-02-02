from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

from ckeditor.fields import RichTextField


@python_2_unicode_compatible
class Slide(models.Model):
    title = models.CharField(max_length=150, blank=True, null=True)
    caption = RichTextField(max_length=500, blank=True, null=True)
    screenshot = models.ImageField(upload_to='preview')
    sortable_order = models.PositiveIntegerField(default=0)

    def get_absolute_url(self):
        return reverse('preview')

    def __str__(self):
        return self.title

    class Meta(object):
        ordering = ('sortable_order',)
        verbose_name = _('Slide')
