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
from typing import List

from django.core.handlers.asgi import ASGIRequest
# Core Django imports
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
# Django Ninja Imports
from ninja import NinjaAPI
from ninja.pagination import paginate
from ninja.responses import Response

from monta import decorators
# Monta Imports
from monta_billing import models, schema

"""
NOTE: Do not add docstrings to this file. Docstrings are added to the generated
documentation for the API. If you add docstrings to this file, they will be
included in the documentation.
"""

api: NinjaAPI = NinjaAPI(csrf=True, version="1.0.0")


@decorators.check_organization(models.ChargeType)
@api.post("/charge_types", tags=["Charge Types"])
def create_charge_type(
    request: ASGIRequest, payload: schema.ChargeTypeIn
) -> schema.ChargeTypeIn:
    """
    Create a new charge type

    Note:
    - **Organization** is set to the organization of the user making the request
    """
    charge_type: models.ChargeType = models.ChargeType.objects.create(
        organization=request.user.profile.organization, **payload.dict()
    )
    return schema.ChargeTypeIn.from_orm(charge_type)


@decorators.check_organization(models.ChargeType)
@api.get(
    "/charge_types/{charge_id}", response=schema.ChargeTypeSchema, tags=["Charge Types"]
)
def get_charge_type(request: ASGIRequest, charge_id: int) -> models.ChargeType:
    """
    Get a charge type by id
    """
    charge_type: models.ChargeType = get_object_or_404(models.ChargeType, pk=charge_id)
    return charge_type


@decorators.check_organization(models.ChargeType)
@api.get("/charge_types", response=List[schema.ChargeTypeSchema], tags=["Charge Types"])
@paginate
def list_charge_types(request: ASGIRequest) -> QuerySet[models.ChargeType] | QuerySet:
    """
    List charge types

    Note:
    - **Organization** is set to the organization of the user making the request
    - **Charge Types** are paginated
    """
    queryset: QuerySet[models.ChargeType] = models.ChargeType.objects.filter(
        organization=request.user.profile.organization
    )
    return queryset


@decorators.check_organization(models.ChargeType)
@api.put("/charge_types/{charge_id}", tags=["Charge Types"])
def update_charge_type(
    request: ASGIRequest, charge_id: int, payload: schema.ChargeTypeSchema
) -> Response | schema.ChargeTypeSchema:
    """
    Update a charge type
    """
    charge_type: models.ChargeType = models.ChargeType.objects.get(
        pk__exact=charge_id, organization=request.user.profile.organization
    )
    for attr, value in payload.dict().items():
        setattr(charge_type, attr, value)
    charge_type.save()
    return schema.ChargeTypeSchema.from_orm(charge_type)


@decorators.check_organization(models.ChargeType)
@api.delete("/charge_types/{charge_id}", tags=["Charge Types"])
def delete_charge_type(request: ASGIRequest, charge_id: int) -> Response:
    """
    Delete a charge type
    """
    charge_type: models.ChargeType = models.ChargeType.objects.get(
        pk__exact=charge_id, organization=request.user.profile.organization
    )
    charge_type.delete()
    return Response({"detail": "Charge type deleted."}, status=204)
