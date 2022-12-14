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

from django.db.models.signals import post_save

# Core Django Libraries
from django.dispatch import receiver

# Monta Imports
from monta_organization import models


@receiver(post_save, sender=models.Organization)
def create_settings(sender, instance, created, **kwargs) -> None:
    """
    Create Organization settings for an organization
    """
    if created:
        models.OrganizationSettings.objects.create(organization=instance)
