from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PreviewConfig(AppConfig):
    name = 'eti_marketing.preview'
    verbose_name = _('Preview')
