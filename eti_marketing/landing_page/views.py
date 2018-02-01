from django.views.generic import DetailView as BaseDetailView

from .models import LandingPage
from eti_marketing.utils import get_base_template


class DetailView(BaseDetailView):
    model = LandingPage
    template_name = 'eti_marketing/landing_page/detail.html'
    context_object_name = 'landing'

    def get_queryset(self):
        queryset = super().get_queryset()

        if not self.request.user.is_superuser:
            queryset = queryset.published()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['base_template'] = get_base_template()
        return context
