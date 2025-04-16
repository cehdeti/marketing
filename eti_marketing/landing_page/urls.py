from django.urls import path

from . import views

urlpatterns = [
    path('<str:slug>/', views.DetailView.as_view(), name='marketing-landing-page'),
]
