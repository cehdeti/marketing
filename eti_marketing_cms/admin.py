from django.contrib import admin
from django.conf import settings
from .models import *

def make_published(modeladmin, request, queryset):
  queryset.update(page_status=True)
make_published.short_description = "Publish Selected Pages"

def make_unpublished(modeladmin, request, queryset):
  queryset.update(page_status=False)
make_unpublished.short_description = "Hide Selected Pages"

@admin.register(Marketing)
class MarketingAdmin(admin.ModelAdmin):
	readonly_fields = ['last_updated']
	prepopulated_fields = {"slug": ["title"]}
	list_display = ['short_title', 'added_date', 'last_updated', 'published']
	list_filter = ['title', 'added_date', 'last_updated', 'published']
	search_fields = ['title']
	actions = [make_published, make_unpublished]
	view_on_site = True
	save_as = True

	fieldsets = (
		(None, {
			'fields': ('title', 'slug', 'last_updated',)
		}),
		('Header', {
			'fields': (('header',), 'subheader',)
		}),
		('Layouts', {
			'fields': ('columns', 'column_1', 'column_2', 'sidebar', 'sidebar_text', 'footer')
		}),
		('Call to Actions', {
			'fields': ('cta', ('cta_text', 'cta_url'), ('socials', 'addthis_pubid'))
		}),
		('Additional SEO', {
			'classes': ('collapse',),
			'fields': ('seo_keywords', 'seo_description')
		}),
		('Page Status', { 'fields': ('published',) })
	)

	def get_changeform_initial_data(self, request):
		return {
			'cta_text': 'Contact Us'
		}