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
from typing import Type

# Core Django Imports
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.base_user import AbstractBaseUser

# Monta Imports
from monta_user.models import MontaUser

UserModel: Type[AbstractBaseUser] = get_user_model()


class MontaBackend(BaseBackend):
    def authenticate(
        self, request, username=None, password=None, **kwargs
    ) -> AbstractBaseUser | None:
        """Authenticate the user session

        Args:
            request (ASGIRequest): The request object
            username (str): The username of the user
            password (str): The password of the user

        Returns:
            AbstractBaseUser | None: The user object or None if the user does not exist
        """
        try:
            user: MontaUser = MontaUser.objects.get(username=username)
            if user.check_password(password):
                return user
            return None
        except MontaUser.DoesNotExist:
            UserModel().set_password(password)
            return None

    def get_user(self, user_id) -> AbstractBaseUser | None:
        """Get the user object

        Args:
            user_id (int): The id of the user

        Returns:
            AbstractBaseUser | None: The user object or None if the user does not exist

        """
        try:
            monta_user = MontaUser.objects.select_related(
                "profile", "profile__title", "profile__organization"
            ).get(pk__exact=user_id)
            return monta_user
        except MontaUser.DoesNotExist:
            return None
