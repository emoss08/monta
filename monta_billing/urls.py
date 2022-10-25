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
from monta_billing import views

app_name = "monta_billing"
urlpatterns = [
    path(
        "interactive/",
        views.InteractiveBillingView.as_view(),
        name="interactive_billing_index",
    ),
]

# Charge Type Urls
urlpatterns += [
    path("charge_type/", views.ChargeTypeListView.as_view(), name="charge_type_index"),
    path(
        "charge_type/create/",
        views.ChargeTypeCreateView.as_view(),
        name="charge_type_create",
    ),
    path(
        "charge_type/update/<str:charge_type_name>/",
        views.ChargeTypeUpdateView.as_view(),
        name="charge_type_update",
    ),
    path(
        "charge_type/delete/<int:pk>/",
        views.ChargeTypeDeleteView.as_view(),
        name="charge_type_delete",
    ),
    path(
        "charge_type/table/",
        views.ChargeTypeOverviewListView.as_view(),
        name="charge_type_table",
    ),
]

# Billing Action Urls
urlpatterns += [
    path(
        "transfer/orders/",
        views.OrderTransferView.as_view(),
        name="transfer_orders_to_billing",
    ),
    path("bill/orders/", views.bill_orders, name="bill_orders"),
    path("re-bill/order/<str:order_id>/", views.re_bill_order, name="re_bill_order"),
]
