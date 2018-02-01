from django.views.generic import (
    ListView as BaseListView,
    DetailView as BaseDetailView,
)

from .models import Article
from eti_marketing.utils import BaseTemplateMixin, PublishedQuerysetMixin


class ListView(PublishedQuerysetMixin, BaseTemplateMixin, BaseListView):
    model = Article
    template_name = 'eti_marketing/news/list.html'


class DetailView(PublishedQuerysetMixin, BaseTemplateMixin, BaseDetailView):
    model = Article
    template_name = 'eti_marketing/news/detail.html'
