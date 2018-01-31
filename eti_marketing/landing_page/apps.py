from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class LandingPageConfig(AppConfig):
    name = 'eti_marketing.landing_page'
    verbose_name = _('Landing Pages')
