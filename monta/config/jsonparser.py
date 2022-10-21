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

import json
from typing import TextIO

file: TextIO = open("monta_config.json", "r")

data = json.load(file)


def get_config() -> dict:
    """
    Returns the config file

    :return: The config file
    :rtype: dict
    """
    return data


def get_google_client_id() -> str:
    """
    Returns the Google client id from the config file

    :return: The Google client id
    :rtype: str
    """
    return data["google_client_id"]


def update_google_client_id(new_id: str) -> None:
    """
    Updates the Google client id in the config file

    :param new_id: The new Google client id
    :type new_id: str
    """
    data["google_client_id"] = new_id
    with open("monta_config.json", "w") as client_id_file:
        json.dump(data, client_id_file)


def get_google_client_secret() -> str:
    """
    Returns the Google client secret from the config file

    :return: The Google client secret
    :rtype: str
    """
    return data["google_client_secret"]


def update_google_client_secret(new_secret: str) -> None:
    """
    Updates the Google client secret in the config file

    :param new_secret: The new Google client secret
    :type new_secret: str
    :return: None
    :rtype: None
    """
    data["google_client_secret"] = new_secret
    with open("monta_config.json", "w") as new_secret_file:
        json.dump(data, new_secret_file)


def get_google_api_key() -> str:
    """
    Returns the google api key from the config file

    :return: The google api key
    :rtype: str
    """
    return data["google_api_key"]


def update_google_api_key(new_key: str) -> None:
    """
    Updates the google api key in the config file

    :param new_key: The new google api key
    :type new_key: str
    :return: None
    :rtype: None
    """
    data["google_api_key"] = new_key
    with open("monta_config.json", "w") as api_key_file:
        json.dump(data, api_key_file)
