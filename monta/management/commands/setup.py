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

# Create tests data for the application

# Core Django Imports
from django.core.management.base import BaseCommand, CommandParser

# Third-Party Imports
from faker import Faker

# Monta Imports
from monta_organization.models import Organization


class Command(BaseCommand):
    help = 'Seeds the database with test data'

    def add_arguments(self, parser: CommandParser):
        parser.add_argument('number_of_organizations', nargs='?', type=int)

    def handle(self, *args, **options) -> None:
        """Seeds the database with test data"""
        number_of_organizations: int = options['number_of_organizations'] or 10
        fake = Faker()
        for i in range(number_of_organizations):
            organization = Organization(
                name=fake.company(),
                description=fake.text(),
                website=fake.url(),
            )
            organization.save()
            self.stdout.write(self.style.SUCCESS(f'Organization {organization.name} created'))
