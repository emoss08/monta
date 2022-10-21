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
# Standard Python Imports
from typing import Literal, Type

# Core Django Imports
from django.contrib import admin

# Monta Imports
from monta_user import models


@admin.register(models.Organization)
class OrganizationInline(admin.ModelAdmin[models.Organization]):
    """Organization Admin"""

    list_display: tuple[str] = ("name", "description", "created", "modified")


@admin.register(models.JobTitle)
class JobTitleInline(admin.ModelAdmin[models.JobTitle]):
    """Job Title Admin"""

    list_display: tuple[str] = ("name", "description", "created", "modified")


@admin.register(models.Profile)
class ProfileUserInline(admin.ModelAdmin[models.Profile]):
    """Profile Admin"""

    list_display: tuple[str] = (
        "user",
        "organization",
        "address_line_1",
        "city",
        "state",
        "zip_code",
        "phone",
        "created",
        "modified",
    )


class ProfileInline(admin.StackedInline[models.Profile]):
    """User Info Inline"""

    model: Type[models.Profile] = models.Profile
    can_delete: Literal[False] = False
    verbose_name_plural: str = "User Info"


@admin.register(models.MontaUser)
class UserInline(admin.ModelAdmin[models.MontaUser]):
    """User Inline"""

    inlines: tuple[Type[ProfileInline]] = (ProfileInline,)
