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

# Standard Library Imports
from typing import Any
import unicodedata

# Core Django Imports
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class MontaUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, user_name: str, email: str, password: str, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        username = user_name.lower()
        if not email:
            raise ValueError(_("The Email must be set"))
        email: str = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self, username: str, email: str, password: str, **extra_fields: Any
    ):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(username, email, password, **extra_fields)

    @classmethod
    def normalize_username(cls, username: str) -> str:
        """
        Normalize the username by removing any non-ASCII characters and
        converting to lowercase.

        Taken from django.contrib.auth.models.AbstractUser.normalize_username

        :param username: The username to normalize
        :type username: str
        :return: The normalized username
        :rtype: str
        """
        return (
            unicodedata.normalize("NFKC", username)
            if isinstance(username, str)
            else username
        )
