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

# Core Django Imports
from django.dispatch import receiver
from django.db.models.signals import post_save

# Monta Imports
from monta_user import models


@receiver(post_save, sender=models.Profile)
def create_profile(sender, instance, created, **kwargs):
    """
    Create a profile for the user
    """
    if created:
        models.Profile.objects.create(user=instance)
