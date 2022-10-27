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
import markdown
from django import template
from django.utils.safestring import SafeString, mark_safe

register = template.Library()


@register.filter(name="markdown")
def markdown_format(text: str) -> SafeString:
    """Convert Markdown to HTML

    Args:
        text (str): Markdown text to convert to HTML

    Returns:
        SafeString: HTML string
    """
    return mark_safe(markdown.markdown(text))
