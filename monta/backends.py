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
from django.db.models.base import ModelBase
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.base_user import AbstractBaseUser

# Monta Imports
from monta_user.models import MontaUser

UserModel: ModelBase = get_user_model()


class MontaBackend(BaseBackend):
    """
    Class to authenticate the user session
    """

    def authenticate(
        self, request, username: str = None, password: str = None, **kwargs: any
    ) -> MontaUser | None:
        """
        Override the authenticate method to authenticate the user session

        :param request: The request object
        :type request: HttpRequest
        :param username: The username of the user
        :type username: str
        :param password: The password of the user
        :type password: str
        :param kwargs: Any other keyword arguments
        :type kwargs: dict
        :return: The user object or None if the user does not exist
        :rtype: AbstractBaseUser | None
        """
        if username is None or password is None:
            return
        try:
            user: MontaUser = UserModel._default_manager.get_by_natural_key(username)
        except MontaUser.DoesNotExist:
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    @staticmethod
    def user_can_authenticate(user: MontaUser) -> bool:
        """
        Check if the user can authenticate.

        Taken from django.contrib.auth.backends.ModelBackend and modified to work with MontaUser

        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.

        :param user: The user object
        :type user: AbstractBaseUser
        :return: True if the user can authenticate, False otherwise
        :rtype: bool
        """
        is_active: bool = getattr(user, "is_active", None)
        return is_active or is_active is None

    def get_user(self, user_id: int) -> MontaUser | None:
        """
        Get the user object

        # TODO - Optimize the query to not return so much data. Use .only() on the ORM query.

        :param user_id: The user id of the user
        :type user_id: int
        :return: The user object or None if the user does not exist
        :rtype: AbstractBaseUser | None
        """
        try:
            user: MontaUser = UserModel._default_manager.select_related(
                "profile", "profile__title", "profile__organization"
            ).get(pk__exact=user_id)
        except MontaUser.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None
