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

from monta_fleet import models
from monta_user.models import MontaUser, Organization


class AddFleetForm(forms.ModelForm):
    organization = forms.ModelChoiceField(
        queryset=Organization.objects.all(),
    )
    name = forms.CharField(max_length=50)
    description = forms.CharField(max_length=255, required=False)
    fleet_manager = forms.ModelChoiceField(queryset=MontaUser.objects.all())
    is_active = forms.ChoiceField(choices=((True, "Yes"), (False, "No")))

    class Meta:
        model: Type[models.Fleet] = models.Fleet
        fields: tuple[str, ...] = ("organization", "name", "description", "fleet_manager", "is_active")
