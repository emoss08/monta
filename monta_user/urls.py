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

from monta_user import views

urlpatterns = [
    path(
        "profile/<int:pk>/overview/",
        views.UserProfileView.as_view(),
        name="user_profile_overview",
    ),
    path(
        "profile/<int:pk>/settings",
        views.UserProfileSettings.as_view(),
        name="user_profile_settings",
    ),
    path(
        "profile/<int:pk>/update",
        views.UpdateUserProfile.as_view(),
        name="user_profile_update",
    ),
    path(
        "profile/<int:pk>/update/email",
        views.UpdateUserEmail.as_view(),
        name="user_profile_email_update",
    ),
    path(
        "profile/<int:pk>/update/password",
        views.UpdateUserPassword.as_view(),
        name="user_profile_password_update",
    ),
]
