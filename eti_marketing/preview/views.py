from django.views.generic import ListView as BaseListView

from .models import Slide
from eti_marketing.utils import get_base_template


class ListView(BaseListView):
    model = Slide
    template_name = 'eti_marketing/preview/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['base_template'] = get_base_template()
        return context
