from __future__ import unicode_literals
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MarketingConfig(AppConfig):
    name = 'eti_marketing'
    verbose_name = _('Marketing')
