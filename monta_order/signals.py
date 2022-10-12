# -*- coding: utf-8 -*-
from django.dispatch import receiver
from django.db.models.signals import post_save
from monta_order import models


@receiver(post_save, sender=models.Stop)
def sequence_stops(sender, instance, created, **kwargs):
    if created:
        instance.movement.sequence_stops()
