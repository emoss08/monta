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

file = open("monta_config.json", "r")

data = json.load(file)


def get_config() -> dict:
    """
    Returns the config file

    Args:
        None

    Returns:
        dict: The config file
    """
    return data


def get_google_client_id() -> str:
    """
    Returns the google client id from the config file

    Args:
        None

    Returns:
        str: The google client id
    """
    return data["google_client_id"]


def update_google_client_id(new_id):
    """
    Updates the google client id in the config file

    Args:
        new_id (str): The new google client id

    Returns:
        None
    """
    data["google_client_id"] = new_id
    with open("monta_config.json", "w") as client_id_file:
        json.dump(data, client_id_file)


def get_google_client_secret() -> str:
    """
    Returns the google client secret from the config file

    Args:
        None

    Returns:
        str: The google client secret
    """
    return data["google_client_secret"]


def update_google_client_secret(new_secret):
    """
    Updates the google client secret in the config file

    Args:
        new_secret (str): The new google client secret

    Returns:
        None
    """
    data["google_client_secret"] = new_secret
    with open("monta_config.json", "w") as new_secret_file:
        json.dump(data, new_secret_file)


def get_google_api_key() -> str:
    """
    Returns the google api key from the config file

    Args:
        None

    Returns:
        str: The google api key
    """
    return data["google_api_key"]


def update_google_api_key(new_key):
    """
    Updates the google api key in the config file

    Args:
        new_key (str): The new google api key

    Returns:
        None
    """
    data["google_api_key"] = new_key
    with open("monta_config.json", "w") as api_key_file:
        json.dump(data, api_key_file)
