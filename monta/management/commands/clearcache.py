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
from django.core.management.base import BaseCommand, CommandParser
from django.conf import settings
from django.core.cache import caches


def clear_cache(cache_name: str):
    """Clears the cache"""
    assert settings.CACHES
    caches[cache_name].clear()


class Command(BaseCommand):
    help = "Clears the cache"

    def add_arguments(self, parser: CommandParser):
        parser.add_argument("cache_name", nargs="?", type=str)

    def handle(self, *args, **options) -> None:
        """Clears the cache"""
        cache_name: str = options["cache_name"] or "default"
        try:
            clear_cache(cache_name)
            self.stdout.write(self.style.SUCCESS(f"Cache {cache_name} cleared"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
