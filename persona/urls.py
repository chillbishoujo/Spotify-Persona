from django.urls import path

from . import views

app_name = 'persona'

urlpatterns = [
    path('', views.home_view, name='index'),
    path('redirect/', views.redirect_view, name='auth'),
    path('app/', views.app, name='app'),
]
