from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.ListView.as_view(), name='news-article-list'),
    url(r'^(?P<slug>[^\.]+)/$', views.DetailView.as_view(), name='news-article-detail'),
]
