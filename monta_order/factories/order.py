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

import factory

from monta_order.models import Order


class OrderFactory(factory.django.DjangoModelFactory):
    """
    Order factory class
    """

    class Meta:
        model: Type[Order] = Order

    organization: factory.SubFactory = factory.SubFactory(
        "monta_organization.factories.organization.OrganizationFactory"
    )
    order_id: factory.Faker = factory.Faker("pyint")
    status: str = "AVAILABLE"
