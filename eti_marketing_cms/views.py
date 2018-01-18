from django.shortcuts import render, get_object_or_404
from django.conf import settings
from pages.models import Page
from .models import Marketing
import os

def marketing_page(request, slug):

	current_page = Page.objects.from_path(request.path, settings.LANGUAGE_CODE)

	if request.user.is_superuser:
		landing = get_object_or_404(Marketing.objects.filter(slug=slug))
	else:
		landing = get_object_or_404(Marketing.objects.filter(published=True), slug=slug)

	current_url = landing.get_absolute_url()

	header_bg_name = os.path.basename(landing.header_bg).split('.')[0]

	cta_html = '<a href="%s" class="page-landing-cta">%s</a>' % (landing.cta_url, landing.cta_text)

	return render(request, 'landing.html', locals())