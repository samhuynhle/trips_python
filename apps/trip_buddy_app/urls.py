from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^dashboard$', views.dashboard_display),
    url(r'^trips/new$', views.create_trip_display),
    url(r'^trips/create$', views.create_trip_process),
    url(r'^trips/edit/(?P<trip_id>[0-9]+)$', views.edit_trip_display),
    url(r'^trips/process_edits/(?P<trip_id>[0-9]+)$', views.edit_trip_process),
    url(r'^trips/(?P<trip_id>[0-9]+)$', views.trip_display),
    url(r'^process/join_trip/(?P<trip_id>[0-9]+)$', views.user_join_trip),
    url(r'^process/leave_trip/(?P<trip_id>[0-9]+)$', views.user_leave_trip),
    url(r'^process/remove_trip/(?P<trip_id>[0-9]+)$', views.remove_trip),
]