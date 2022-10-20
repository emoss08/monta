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

# Standard Python Libraries
from typing import Type

# Core Django imports
from django.contrib import admin

# Monta Imports
from monta_customer import models


class CustomerBillingProfileInline(admin.StackedInline[models.CustomerBillingProfile]):
    """CustomerBillingProfile Inline"""
    model: Type[models.CustomerBillingProfile] = models.CustomerBillingProfile
    extra: int = 0


class CustomerContactInline(admin.TabularInline[models.CustomerContact]):
    """
    CustomerContactInline class
    """

    model: Type[models.CustomerContact] = models.CustomerContact
    extra: int = 0


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin[models.Customer]):
    """
    CustomerAdmin class
    """

    list_display = (
        "customer_id",
        "name",
        "address_line_1",
        "address_line_2",
        "city",
        "state",
        "zip_code",
    )
    list_filter = ("is_active", "state")
    search_fields = (
        "customer_id",
        "name",
        "address_line_1",
        "address_line_2",
        "city",
        "state",
        "zip_code",
    )
    ordering = ("customer_id",)
    inlines: tuple[Type[CustomerBillingProfileInline], Type[CustomerContactInline]] = (
        CustomerBillingProfileInline, CustomerContactInline
    )


@admin.register(models.DocumentClassification)
class DocumentClassificationAdmin(admin.ModelAdmin[models.DocumentClassification]):
    """
    DocumentClassificationAdmin class
    """

    list_display = ("name", "description")
    search_fields = ("name", "description")
    ordering = ("name",)
