from django.conf.urls import include, url


urlpatterns = [
    url(r'^', include('eti_marketing_cms.landing_page.urls')),
]
