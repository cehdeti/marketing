from django.views.generic import DetailView

from .models import LandingPage
from eti_marketing.utils import get_base_template


class LandingPageView(DetailView):
    template_name = 'eti_marketing/landing_page/detail.html'
    context_object_name = 'landing'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return LandingPage.objects.all()
        else:
            return LandingPage.objects.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['base_template'] = get_base_template()
        return context
