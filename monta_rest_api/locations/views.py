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

# Core Django Imports
from rest_framework import viewsets, status, permissions
from rest_framework.request import Request
from rest_framework.response import Response

# Monta Imports
from monta_locations import models
from monta_rest_api.locations import serializers


class LocationViewSet(viewsets.ModelViewSet):
    """
    Location View Set
    """

    queryset = models.Location.objects.all()
    serializer_class: Type[
        serializers.LocationSerializer
    ] = serializers.LocationSerializer
    permission_classes: list[Type[permissions.IsAuthenticated]] = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        """
        This view should return a list of all the locations
        for the currently authenticated user.
        """
        return models.Location.objects.filter(
            organization=self.request.user.profile.organization
        )

    def update(
        self, request: Request, pk: int | None = None, *args, **kwargs
    ) -> Response:
        """
        Update a location

        Args:
            request (Request): The request object
            pk (int, optional): The primary key of the location. Defaults to None.
            *args: The list of arguments
            **kwargs: The dictionary of keyword arguments
        """
        instance: models.Location = self.get_object()
        instance.organization = self.request.user.profile.organization
        serializer: serializers.LocationSerializer = self.get_serializer(
            instance, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LocationContactViewSet(viewsets.ModelViewSet):
    """
    Location Contact View Set
    """

    queryset = models.LocationContact.objects.all()
    serializer_class: Type[
        serializers.LocationContactSerializer
    ] = serializers.LocationContactSerializer
    permission_classes: list[Type[permissions.IsAuthenticated]] = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        """
        This view should return a list of all the location contacts
        for the currently authenticated user.
        """
        return models.LocationContact.objects.filter(
            organization=self.request.user.profile.organization
        )

    def update(
        self, request: Request, pk: int | None = None, *args, **kwargs
    ) -> Response:
        """
        Update a location contact

        Args:
            request (Request): The request object
            pk (int, optional): The primary key of the location contact. Defaults to None.
            *args: The list of arguments
            **kwargs: The dictionary of keyword arguments
        """
        instance: models.LocationContact = self.get_object()
        instance.organization = self.request.user.profile.organization
        serializer: serializers.LocationContactSerializer = self.get_serializer(
            instance, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
