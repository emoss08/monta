# -*- coding: utf-8 -*-
from django.apps import AppConfig


class MontaOrderConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "monta_order"

    def ready(self):
        import monta_order.signals
