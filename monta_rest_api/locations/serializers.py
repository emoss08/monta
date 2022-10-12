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
from typing import Type

# Django Rest Framework Imports
from rest_framework import serializers

# Monta Imports
from monta_locations import models


class LocationSerializer(serializers.ModelSerializer):
    """
    Location Serializer
    """

    contacts = serializers.HyperlinkedRelatedField(
        read_only=True,
        many=True,
        view_name="locationcontact-detail",
    )

    class Meta:
        """
        Meta Class for Location Serializer
        """

        model: Type[models.Location] = models.Location
        fields = "__all__"


class LocationContactSerializer(serializers.ModelSerializer):
    """
    Location Contact Serializer
    """

    class Meta:
        """
        Meta Class for Location Contact Serializer
        """

        model: Type[models.LocationContact] = models.LocationContact
        fields = "__all__"
