from django.views.generic import DetailView, FormView
from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import ugettext_lazy as _
from django.utils.module_loading import import_string

from .models import LandingPage


def _get_base_template():
    return getattr(settings, 'ETI_MARKETING_CMS_BASE_TEMPLATE', 'base.html')


class LandingPageView(DetailView):
    template_name = 'eti_marketing_cms/landing.html'
    context_object_name = 'landing'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return LandingPage.objects.all()
        else:
            return LandingPage.objects.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['base_template'] = _get_base_template()
        return context


class SignupView(SuccessMessageMixin, FormView):
    template_name = 'eti_marketing_cms/signup.html'
    success_message = _('Thank you for signing up! We\'ll get back to you shortly.')

    def get_form_class(self):
        cls = getattr(settings, 'ETI_MARKETING_CMS_SIGNUP_FORM_CLASS', 'eti_marketing_cms.forms.SignupForm')
        return import_string(cls)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.get_full_path()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['base_template'] = _get_base_template()
        return context
