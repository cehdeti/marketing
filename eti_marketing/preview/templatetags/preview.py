from django import template
register = template.Library()


@register.inclusion_tag('eti_marketing/preview/_slideshow.html')
def preview_slideshow(slides):
    return {'slides': slides}
