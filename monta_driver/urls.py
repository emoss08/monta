# -*- coding: utf-8 -*-
"""
COPYRIGHT 2022 MONTA

This file is part of Monta.

Monta is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Monta is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Monta.  If not, see <https://www.gnu.org/licenses/>.
"""
# Core Django Imports
from django.urls import path

# Monta Core Imports
from monta_driver import views, feeds

urlpatterns = [
    path("", views.DriverListView.as_view(), name="driver_overview"),
    path("table/", views.DriverOverviewList.as_view(), name="driver_table"),
    path("create/", views.DriverCreateView.as_view(), name="driver_create"),
    path("<int:pk>/edit/", views.DriverEditView.as_view(), name="driver_edit"),
    path("<int:pk>/delete/", views.DriverDeleteView.as_view(), name="driver_delete"),
    path("feed/", feeds.LatestDriverFeed(), name="driver_feed"),
    path("search/", views.DriverSearchView.as_view(), name="driver_post_search"),
    path(
        "validate/license_number/",
        views.validate_license_number,
        name="validate_license_number",
    ),
]
