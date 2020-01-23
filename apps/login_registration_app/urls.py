from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^success$', views.success),
    url(r'^createuser$', views.create),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^$', views.home),
]