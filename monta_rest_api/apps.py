# -*- coding: utf-8 -*-
from django.apps import AppConfig


class MontaRestApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "monta_rest_api"

    # def ready(self):
    #     import monta_rest_api.signals
