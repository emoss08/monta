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

from typing import Type

from django.contrib import admin

from monta_customer import models


class CustomerBillingProfileInline(admin.StackedInline):
    """CustomerBillingProfile Inline"""

    model: Type[models.CustomerBillingProfile] = models.CustomerBillingProfile
    extra: int = 0


class CustomerContactInline(admin.TabularInline):
    """
    CustomerContactInline class
    """

    model: Type[models.CustomerContact] = models.CustomerContact
    extra: int = 0


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    """
    CustomerAdmin class
    """

    list_display: tuple[str, ...] = (
        "customer_id",
        "name",
        "address_line_1",
        "address_line_2",
        "city",
        "state",
        "zip_code",
    )
    list_filter: tuple[str, ...] = ("is_active", "state")
    search_fields: tuple[str, ...] = (
        "customer_id",
        "name",
        "address_line_1",
        "address_line_2",
        "city",
        "state",
        "zip_code",
    )
    ordering: tuple[str, ...] = ("customer_id",)
    inlines: tuple[Type[CustomerBillingProfileInline], Type[CustomerContactInline]] = (
        CustomerBillingProfileInline,
        CustomerContactInline,
    )


@admin.register(models.DocumentClassification)
class DocumentClassificationAdmin(admin.ModelAdmin):
    """
    DocumentClassificationAdmin class
    """

    list_display: tuple[str, ...] = ("name", "description")
    search_fields: tuple[str, ...] = ("name", "description")
    ordering: tuple[str] = ("name",)
