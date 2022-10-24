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

from django.urls import path

from monta_fleet import views

urlpatterns = [
    path("", views.FleetListView.as_view(), name="fleet_overview"),
    path("create/", views.CreateFleet.as_view(), name="fleet_create"),
    path("<int:pk>/edit/", views.FleetEditView.as_view(), name="fleet_edit"),
    path("<int:pk>/delete/", views.delete_fleet, name="fleet_delete"),
    path("table/", views.FleetOverviewList.as_view(), name="fleet_table"),
]
