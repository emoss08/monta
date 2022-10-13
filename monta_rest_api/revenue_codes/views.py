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
from django.db.models import QuerySet

# Rest Framework Imports
from rest_framework import viewsets, status, permissions
from rest_framework.request import Request
from rest_framework.response import Response

# Monta Imports
from monta_order import models
from monta_rest_api.revenue_codes import serializers


class RevenueCodeView(viewsets.ModelViewSet):
    """
    Revenue Code ModelViewSet
    """

    queryset = models.RevenueCode.objects.all()
    serializer_class: Type[
        serializers.RevenueCodeSerializer
    ] = serializers.RevenueCodeSerializer
    permission_classes: list[Type[permissions.IsAuthenticated]] = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self) -> QuerySet[models.RevenueCode]:
        """
        Get the revenue code for the user by organization

        :return: Queryset of the Revenue Codes
        :rtype: QuerySet[models.RevenueCode]
        """
        return models.RevenueCode.objects.filter(
            oranization__exact=self.request.user.profile.organization
        )

    def create(self, request: Request, *args: list, **kwargs: dict) -> Response:
        """
        Create a new Revenue Code

        :param request: Request Object
        :type request: Request
        :param args
        :type args: list
        :param kwargs
        :type kwargs: dict
        :returns: Response with response code 201 or 400
        :rtype: Response
        """

        serializer: serializers.RevenueCodeSerializer = self.serializer_class(
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(
        self,
        request: Request,
        pk: int | None = None,
        *args: list,
        **kwargs: dict,
    ) -> Response:
        """
        Get a Delay Code by id

        :param request: Request Object
        :type request: Request
        :param pk
        :type pk: int | None
        :param args
        :type args: list
        :param kwargs
        :type kwargs: dict
        :returns: Response with response code 201 or 400
        :rtype: Response
        """

        revenue_code: models.RevenueCode = self.get_object()
        serializer: serializers.RevenueCodeSerializer = self.serializer_class(
            revenue_code
        )
        return Response(serializer.data)

    def update(self, request: Request, *args: list, **kwargs: dict) -> Response:
        """
        Update a Delay Code

        :param request: Request Object
        :type request: Request
        :param args
        :type args: list
        :param kwargs
        :type kwargs: dict
        :returns: Response with response code 201 or 400
        :rtype: Response
        """

        revenue_code: models.RevenueCode = self.get_object()
        serializer: serializers.RevenueCodeSerializer = self.serializer_class(
            revenue_code, data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(
        self,
        request: Request,
        pk: int | None = None,
        *args: list,
        **kwargs: dict,
    ) -> Response:
        """
        Update a Delay Code

        Args:
            request (Request): The request object
            pk (int | None, optional): The id of the delay code. Defaults to None.
        """

        revenue_code: models.RevenueCode = self.get_object()
        serializer: serializers.RevenueCodeSerializer = self.serializer_class(
            revenue_code, data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
