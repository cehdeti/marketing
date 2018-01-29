from __future__ import unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^p/(?P<slug>[^\.]+)/', views.LandingPageView.as_view(), name='marketing-landing-page'),
]
