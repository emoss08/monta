# -*- coding: utf-8 -*-
from django.apps import AppConfig


class MontaOrganizationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "monta_organization"

    def ready(self):
        from monta_organization import signals
