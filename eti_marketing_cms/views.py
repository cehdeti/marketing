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

	context = {
		'current_url': current_url,
		'current_page': current_page,
		'header_bg_name': header_bg_name,
		'landing': landing,
	}

	return render(request, 'eti_marketing_cms/landing.html', context)