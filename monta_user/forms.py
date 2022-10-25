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

from django import forms

from monta_user.models import Profile, MontaUser


class UpdateProfileGeneralInformationForm(forms.ModelForm):
    """Update User General Information form validation."""

    first_name = forms.CharField(max_length=255, help_text="First name of the user")
    last_name = forms.CharField(max_length=255, help_text="Last name of the user")
    profile_picture = forms.ImageField(required=False)
    address = forms.CharField(
        max_length=100, help_text="Address for the user", required=False
    )
    city = forms.CharField(
        max_length=255, help_text="City for the user", required=False
    )
    state = forms.CharField(
        max_length=2, help_text="State for the user", required=False
    )
    zip_code = forms.IntegerField(help_text="Zip code for the user", required=False)
    phone = forms.CharField(
        max_length=10, help_text="Phone Number for user", required=False
    )

    class Meta:
        """Update User General Information META"""

        model: Type[Profile] = Profile
        fields: tuple[str, ...] = (
            "profile_picture",
            "first_name",
            "last_name",
            "address",
            "city",
            "state",
            "zip_code",
            "phone",
        )


class UpdateUserEmailForm(forms.ModelForm):
    """Update User Email form validation."""

    email = forms.EmailField(max_length=255, help_text="Email for the user")
    password = forms.CharField(max_length=255, help_text="Password for the user")

    class Meta:
        """Update User Email META"""

        model: Type[MontaUser] = MontaUser
        fields: list[str] = ["email"]


class UpdateUserPasswordForm(forms.ModelForm):
    """Update User password form validation."""

    current_password = forms.CharField(
        max_length=255, help_text="Password for the user"
    )
    password = forms.CharField(max_length=255, help_text="New password for the user")

    class Meta:
        """Update User Password META"""

        model: Type[MontaUser] = MontaUser
        fields: list[str] = ["current_password", "password"]
