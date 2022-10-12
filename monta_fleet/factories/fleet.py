# -*- coding: utf-8 -*-
import factory

from monta_fleet.models import Fleet


class FleetFactory(factory.django.DjangoModelFactory):
    """
    Fleet factory class
    """

    class Meta:
        model = Fleet

    organization = factory.SubFactory(
        "monta_user.factories.organization.OrganizationFactory"
    )
    name = factory.Faker("name")
    fleet_id = factory.Faker("pyint")
    description = factory.Faker("text")
    fleet_manager = factory.SubFactory("monta_user.factories.user.MontaUserFactory")
    is_active = factory.Faker("boolean")
