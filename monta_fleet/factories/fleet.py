# -*- coding: utf-8 -*-
from typing import Type

import factory

from monta_fleet.models import Fleet


class FleetFactory(factory.django.DjangoModelFactory):
    """
    Fleet factory class
    """

    class Meta:
        model: Type[Fleet] = Fleet

    organization: factory.SubFactory = factory.SubFactory(
        "monta_user.factories.organization.OrganizationFactory"
    )
    name: factory.Faker = factory.Faker("name")
    fleet_id: factory.Faker = factory.Faker("pyint")
    description: factory.Faker = factory.Faker("text")
    fleet_manager: factory.Faker = factory.SubFactory("monta_user.factories.user.MontaUserFactory")
    is_active: factory.Faker = factory.Faker("boolean")
