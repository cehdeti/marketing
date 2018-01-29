from django.views.generic import DetailView as BaseDetailView
from django.conf import settings
from .models import LandingPage


class DetailView(BaseDetailView):
    template_name = 'eti_marketing_cms/landing.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return LandingPage.objects.all()
        else:
            return LandingPage.objects.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['base_template'] = getattr(settings, 'ETI_MARKETING_CMS_BASE_TEMPLATE', 'base.html')
        return context
