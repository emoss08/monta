# -*- coding: utf-8 -*-
from django.urls import path

from monta_routes import views

app_name = 'monta_routes'
urlpatterns = [
    path("geocode_locations/", views.geocode_locations, name="geocode_locations"),
    # path(
    #     "get_route_details/<str:origin>/<str:destination>/",
    #     views.get_route_details,
    #     name="get_route_details"
    # )
]
