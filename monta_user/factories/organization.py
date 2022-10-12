# -*- coding: utf-8 -*-
import factory

from monta_user.models import Organization


class OrganizationFactory(factory.django.DjangoModelFactory):
    """
    Organization factory class
    """

    class Meta:
        model = Organization

    name = factory.Faker("company")
