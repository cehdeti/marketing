from django.views.generic import FormView
from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import ugettext_lazy as _
from django.utils.module_loading import import_string

from .utils import get_base_template


class SignupView(SuccessMessageMixin, FormView):
    template_name = 'eti_marketing/signup.html'
    success_message = _("Thank you for signing up! We'll get back to you shortly.")

    def get_form_class(self):
        cls = getattr(settings, 'ETI_MARKETING_SIGNUP_FORM_CLASS', 'eti_marketing.forms.SignupForm')
        return import_string(cls)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.get_full_path()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['base_template'] = get_base_template()
        return context
