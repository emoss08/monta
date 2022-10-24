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
# Core Django imports
from django.contrib.sitemaps import Sitemap

# Monta imports
from monta_driver import models


class DriverSitemap(Sitemap):
    """Driver Site Map"""

    change_freq: str = "monthly"
    priority = 0.9

    def items(self):
        """Return list of drivers"""
        return models.Driver.objects.all()

    def lastmod(self, obj):
        """Last Modified"""
        return obj.updated_at
