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
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy

# Third Party Imports
import markdown

# Monta Imports
from monta_driver import models


class LatestDriverFeed(Feed):
    title = "Latest Drivers"
    link = reverse_lazy("driver_overview")
    description = "Latest Drivers"

    def items(self):
        """Return the last 5 published posts."""
        return models.Driver.objects.all()[:5]

    def item_title(self, item) -> str:
        return f"{item.first_name} {item.last_name}"

    def item_description(self, item) -> str:
        full_name: str = f"{item.first_name} {item.last_name}"
        return truncatewords_html(markdown.markdown(full_name), 30)

    def item_link(self, item) -> str:
        return reverse_lazy("driver_edit", args=[item.pk])
