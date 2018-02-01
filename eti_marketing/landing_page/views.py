from django.views.generic import DetailView as BaseDetailView

from .models import LandingPage
from eti_marketing.utils import BaseTemplateMixin, PublishedQuerysetMixin


class DetailView(PublishedQuerysetMixin, BaseTemplateMixin, BaseDetailView):
    model = LandingPage
    template_name = 'eti_marketing/landing_page/detail.html'
    context_object_name = 'landing'
