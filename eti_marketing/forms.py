from django import forms
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from . import active_campaign


class _TelInput(forms.widgets.TextInput):
    input_type = 'tel'


class _TelField(forms.fields.CharField):
    widget = _TelInput
    default_validators = [
        validators.RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message=_('Phone number must be entered in the format: "+999999999". Up to 15 digits allowed.'),
        )
    ]


class SignupForm(forms.Form):

    first_name = forms.CharField(label=_('First Name'), max_length=100)
    last_name = forms.CharField(label=_('Last Name'), max_length=100)
    organization = forms.CharField(max_length=100)
    title = forms.CharField(label=_('Job Title'), max_length=100)
    email = forms.EmailField(label=_('E-mail Address'))
    phone = _TelField(label=_('Phone Number'), required=False)

    def save(self):
        result = active_campaign.save_contact(**self.get_active_campaign_payload())

        event = self.get_active_campaign_event()
        if event:
            active_campaign.track_event(self.cleaned_data['email'], event)

        return result

    def get_active_campaign_payload(self):
        data = self.cleaned_data

        return {
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'orgname': data['organization'],
            'field[%TITLE%,0]': data['title'],
            'email': data['email'],
            'phone': data.get('phone'),
        }

    def get_active_campaign_event(self):
        return getattr(settings, 'ACTIVE_CAMPAIGN_SIGNUP_EVENT', None)
