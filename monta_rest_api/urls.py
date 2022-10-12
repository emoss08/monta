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

# Standard library Imports
from django.urls import path, include
from rest_framework import routers

# Rest Framework Imports
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

# Monta Imports
from monta_rest_api.users import views as user_views
from monta_rest_api.charge_types import views as charge_type_views
from monta_rest_api.locations import views as location_views
from monta_rest_api.delay_codes import views as delay_code_views
from monta_rest_api.auth.views import (
    auth_token_view,
    refresh_auth_token_view,
    revoke_token_view,
    verify_auth_token_view,
)

router = routers.DefaultRouter()
router.register(r"users", user_views.UserViewSet)
router.register(r"charge_types", charge_type_views.ChargeTypeViewSet)
router.register(r"locations", location_views.LocationViewSet)
router.register(r"location_contacts", location_views.LocationContactViewSet)
router.register(r"delay_codes", delay_code_views.DelayCodeViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("auth/token/", auth_token_view, name="token_obtain_pair"),
    path("auth/token/verify/", verify_auth_token_view, name="token_verify"),
    path("auth/token/refresh/", refresh_auth_token_view, name="token_refresh"),
    path("auth/token/revoke/", revoke_token_view, name="token_revoke"),
]
