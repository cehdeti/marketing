from django.conf.urls import include, url


urlpatterns = [
    url(r'^', include('eti_marketing.landing_page.urls')),
]
