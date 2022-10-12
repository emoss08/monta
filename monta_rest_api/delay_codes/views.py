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
from monta_order.models import DelayCode
from monta_rest_api.delay_codes import serializers


class DelayCodeViewSet(viewsets.ModelViewSet):
    """
    Delay Code View Set
    """

    queryset = DelayCode.objects.all()
    serializer_class: Type[
        serializers.DelayCodeSerializer
    ] = serializers.DelayCodeSerializer
    permission_classes: list[Type[permissions.IsAuthenticated]] = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        """
        This view should return a list of all the delay codes
        for the currently authenticated user.
        """
        return DelayCode.objects.filter(
            organization=self.request.user.profile.organization
        )

    def create(self, request: Request, *args, **kwargs) -> Response:
        """
        Create a new Delay Code

        Args:
            request (Request): The request object
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The response object
        """

        serializer: serializers.DelayCodeSerializer = self.serializer_class(
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(
        self, request: Request, pk: int | None = None, *args, **kwargs
    ) -> Response:
        """
        Get a Delay Code by id

        Args:
            request (Request): The request object
            pk (int | None, optional): The id of the delay code. Defaults to None.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The response object
        """

        delay_code: DelayCode = self.get_object()
        serializer: serializers.DelayCodeSerializer = self.serializer_class(delay_code)
        return Response(serializer.data)

    def update(self, request: Request, *args, **kwargs) -> Response:
        """
        Update a Delay Code

        Args:
            request (Request): The request object
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The response object
        """

        delay_code: DelayCode = self.get_object()
        serializer: serializers.DelayCodeSerializer = self.serializer_class(
            delay_code, data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(
        self, request, pk: int | None = None, *args, **kwargs
    ) -> Response:
        """
        Update a Delay Code

        Args:
            request (Request): The request object
            pk (int | None, optional): The id of the delay code. Defaults to None.
        """

        delay_code: DelayCode = self.get_object()
        serializer: serializers.DelayCodeSerializer = self.serializer_class(
            delay_code, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
