from django.urls import include, path


urlpatterns = [
    path('p/', include('eti_marketing.landing_page.urls')),
    path('preview/', include('eti_marketing.preview.urls')),
]
