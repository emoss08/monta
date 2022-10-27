# -*- coding: utf-8 -*-
import datetime

import factory
from django.utils import timezone

from monta_user.models import JobTitle, MontaUser, Profile


class JobTitleFactory(factory.django.DjangoModelFactory):
    """
    Job title factory class
    """

    class Meta:
        model = JobTitle

    name = factory.Faker("job")


class MontaUserFactory(factory.django.DjangoModelFactory):
    """
    Monta user factory class
    """

    class Meta:
        model = MontaUser

    username = factory.Faker("user_name")
    password = factory.Faker("password")
    email = factory.Faker("email")
    is_staff = factory.Faker("boolean")
    date_joined = factory.Faker("date_time", tzinfo=timezone.get_current_timezone())

    @factory.post_generation
    def profile(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for profile in extracted:
                self.profile.add(profile)


class ProfileFactory(factory.django.DjangoModelFactory):
    """
    Profile factory class
    """

    class Meta:
        model = Profile

    user = factory.SubFactory(MontaUserFactory)
    organization = factory.SubFactory(
        "monta_user.factories.organization.OrganizationFactory"
    )
    title = factory.SubFactory(JobTitleFactory)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email_verified = factory.Faker("boolean")
    phone = factory.Faker("phone_number")
    address = factory.Faker("address")
    city = factory.Faker("city")
    state = factory.Faker("state_abbr")
    zip_code = factory.Faker("zipcode")
