from __future__ import unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<slug>[^\.]+)/$', views.DetailView.as_view(), name='marketing-landing-page'),
]
