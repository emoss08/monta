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

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models.base import ModelBase

from core.exceptions import UserNotFound
from monta_user.models import MontaUser

UserModel: ModelBase = get_user_model()


class MontaBackend(ModelBackend):
    """
    Class to authenticate the user session
    """

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
        except UserNotFound:
            return None
        return user if self.user_can_authenticate(user) else None
