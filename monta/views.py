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

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_safe
from django.views.decorators.vary import vary_on_cookie
# Core Django Imports
from django.views.generic import TemplateView


@method_decorator(require_safe, name="dispatch")
@method_decorator(cache_control(max_age=60 * 60 * 24), name="dispatch")
@method_decorator(vary_on_cookie, name="dispatch")
class HomePage(LoginRequiredMixin, TemplateView):
    """
    Class to render homepage.

    # TODO: Pop the cache if something changes.
    """

    template_name: str = "homepage/index.html"
