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
from rest_framework import viewsets, status
from rest_framework.request import Request
from rest_framework.response import Response

# Core Django Imports
from django.db.models import QuerySet
from django.http import QueryDict

# Monta Imports
from monta_billing.models import ChargeType
from monta_rest_api.charge_types import serializers


class ChargeTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = ChargeType.objects.all()
    serializer_class: Type[
        serializers.ChargeTypeSerializer
    ] = serializers.ChargeTypeSerializer

    def get_queryset(self) -> QuerySet[ChargeType]:
        """
        This view should return a list of all the charge types
        for the currently authenticated user.
        """
        return ChargeType.objects.filter(
            organization=self.request.user.profile.organization
        )

    def update(self, request: Request, pk: int = None, *args, **kwargs) -> Response:
        """
        Update a charge type

        Args:
            request (Request): The request object
            pk (int): The primary key of the charge type to update
            *args: The list of arguments
            **kwargs: The dictionary of keyword arguments
        """
        instance: ChargeType = self.get_object()

        # Append the organization to the instance
        instance.organization = self.request.user.profile.organization

        data: QueryDict = request.data

        serializer: serializers.ChargeTypeSerializer = self.get_serializer(
            instance, data=data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
