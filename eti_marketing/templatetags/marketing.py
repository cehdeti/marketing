from django.conf import settings

from django import template
register = template.Library()


@register.inclusion_tag('eti_marketing/_ga.html')
def google_analytics():
    return {'id': getattr(settings, 'GOOGLE_ANALYTICS_ID', None)}


@register.inclusion_tag('eti_marketing/_gtm.html')
def google_tagmanager():
    return {'id': getattr(settings, 'GOOGLE_TAGMANAGER_ID', None)}


@register.inclusion_tag('eti_marketing/_gtm_noscript.html')
def google_tagmanager_noscript():
    return {'id': getattr(settings, 'GOOGLE_TAGMANAGER_ID', None)}


@register.inclusion_tag('eti_marketing/_ac.html')
def active_campaign_event_tracker():
    return {'id': getattr(settings, 'ACTIVE_CAMPAIGN_EVENT_ACTID', None)}
