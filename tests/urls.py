from django.conf.urls import include, url


urlpatterns = [
    url(r'^p/', include('eti_marketing.landing_page.urls')),
]
