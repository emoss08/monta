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

# Standard library imports
from typing import List, Type

# Core Django imports
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.core.handlers.asgi import ASGIRequest

# Django Ninja Imports
from ninja import ModelSchema, NinjaAPI

# Monta Imports
from monta_billing import models

api = NinjaAPI(csrf=True, version='1.0.0')


class ChargeTypeSchema(ModelSchema):
    """
    ChargeTypeSchema
    """

    class Config:
        """
        Config class
        """
        model: Type[models.ChargeType] = models.ChargeType
        model_fields: list[str] = ['id', 'name', 'description']


@api.post("/charge_types")
def create_charge_type(request: ASGIRequest, payload: ChargeTypeSchema) -> ChargeTypeSchema:
    """
    Create a new charge type

    :param request: Django request object
    :type request: Request
    :param payload: Incoming payload
    :type payload: ChargeTypeIn
    :return: Outgoing payload
    :rtype: ChargeTypeOut
    """
    charge_type = models.ChargeType.objects.create(organization=request.user.profile.organization, **payload.dict())
    return ChargeTypeSchema.from_orm(charge_type)


@api.get("/charge_types/{charge_id}", response=ChargeTypeSchema)
def get_charge_type(request: ASGIRequest, charge_id: int) -> models.ChargeType:
    """
    Get a charge type by id

    :param request: Django request object
    :type request: Request
    :param charge_id: Charge type id
    :type charge_id: int
    :return: Charge type object
    :rtype: models.ChargeType
    """
    charge_type: models.ChargeType = get_object_or_404(models.ChargeType, pk=charge_id)
    return charge_type


@api.get("/charge_types", response=List[ChargeTypeSchema])
def list_charge_types(request: ASGIRequest) -> QuerySet[models.ChargeType] | QuerySet:
    """
    List Charge Types

    :param request: Django request object
    :type request: Request
    :return: QuerySet of Charge Types
    :rtype: QuerySet[models.ChargeType] | QuerySet
    """
    qs: QuerySet[models.ChargeType] = models.ChargeType.objects.filter(organization=request.user.profile.organization)
    return qs


@api.put("/charge_types/{charge_id}")
def update_charge_type(request: ASGIRequest, charge_id: int, payload: ChargeTypeSchema) -> ChargeTypeSchema:
    """
    Update a charge type

    :param request: Django request object
    :type request: Request
    :param charge_id: Charge type id
    :type charge_id: int
    :param payload: Incoming payload
    :type payload: ChargeTypeIn
    :return: Outgoing payload
    :rtype: ChargeTypeOut
    """
    charge_type: models.ChargeType = get_object_or_404(models.ChargeType, pk=charge_id)
    for attr, value in payload.dict().items():
        setattr(charge_type, attr, value)
    charge_type.save()
    return ChargeTypeSchema.from_orm(charge_type)


@api.delete("/charge_types/{charge_id}")
def delete_charge_type(request: ASGIRequest, charge_id: int) -> dict[str, str]:
    """
    Delete a charge type

    :param request: Django request object
    :type request: Request
    :param charge_id: Charge type id
    :type charge_id: int
    :return: None
    :rtype: None
    """
    charge_type: models.ChargeType = get_object_or_404(models.ChargeType, pk=charge_id)
    charge_type.delete()
    return {"message": "Charge type deleted successfully"}
