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
# Standard Python Libraries
import uuid

# Third Party Libraries
import httpx

# Django Imports
from django.conf import settings
from httpx import Response


def download_image_from_url(url: str) -> None | str:
    """
    Download an image from a url and save it in the media folder.

    :param url: The url of the image to download.
    :type url: str
    :return: The path of the image in the media folder.
    :rtype: str
    """
    extension = url.rsplit(".", 1)[1].lower()
    image_name = f"{uuid.uuid4()}.{extension}"
    media_path = settings.MEDIA_ROOT / "downloaded_images" / image_name
    try:
        response: Response = httpx.get(url)
        response.raise_for_status()
    except httpx.HTTPError as image_exc:
        return f"An Error occurred while download the image: {image_exc}"
    else:
        media_path.parent.mkdir(exist_ok=True, parents=True)
        media_path.write_bytes(response.content)
        return str(media_path)
