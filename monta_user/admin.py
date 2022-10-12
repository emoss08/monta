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
from monta_user.models import MontaUser, Organization, Profile, JobTitle


@admin.register(Organization)
class OrganizationInline(admin.ModelAdmin):
    """Organization Admin"""

    list_display = ("name", "description", "created", "modified")


@admin.register(JobTitle)
class JobTitleInline(admin.ModelAdmin):
    """Job Title Admin"""

    list_display = ("name", "description", "created", "modified")


@admin.register(Profile)
class ProfileUserInline(admin.ModelAdmin):
    """Profile Admin"""

    list_display = (
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


class ProfileInline(admin.StackedInline):
    """User Info Inline"""

    model: Type[Profile] = Profile
    can_delete: Literal[False] = False
    verbose_name_plural: Literal["User Info"] = "User Info"


@admin.register(MontaUser)
class UserInline(admin.ModelAdmin):
    """User Inline"""

    inlines: tuple[Type[ProfileInline]] = (ProfileInline,)
