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
from django.contrib import admin

# Monta Imports
from monta_billing import models


@admin.register(models.ChargeType)
class ChargeTypeAdmin(admin.ModelAdmin[models.ChargeType]):
    """
    ChargeType Admin
    """

    list_display: tuple[str, ...] = (
        "name",
        "description",
    )
    search_fields: tuple[str, ...] = (
        "name",
        "description",
    )


@admin.register(models.AdditionalCharge)
class AdditionalChargeAdmin(admin.ModelAdmin[models.AdditionalCharge]):
    """
    Admin for AdditionalCharge model
    """

    list_display: tuple[str, ...] = (
        "order",
        "charge_type",
        "amount",
        "description",
    )
    search_fields: tuple[str, ...] = (
        "order",
        "charge_type",
        "amount",
        "description",
    )


@admin.register(models.BillingQueue)
class BillingQueueAdmin(admin.ModelAdmin[models.BillingQueue]):
    """
    Admin for BillingQueue
    """

    list_display: tuple[str] = ("order",)
    search_fields: tuple[str] = ("order",)


@admin.register(models.BillingHistory)
class BillingHistoryAdmin(admin.ModelAdmin[models.BillingHistory]):
    """
    Billing History Admin
    """

    list_display: tuple[str, ...] = (
        "batch_name",
        "order",
    )
    search_fields: tuple[str, ...] = (
        "batch_name",
        "order",
    )


@admin.register(models.BillingException)
class BillingExceptionAdmin(admin.ModelAdmin[models.BillingException]):
    """
    Admin for BillingException
    """

    list_display: tuple[str, ...] = (
        "order",
        "exception_type",
        "exception_message",
    )
    search_fields: tuple[str, ...] = (
        "order",
        "exception_type",
        "exception_message",
    )
