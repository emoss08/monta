# -*- coding: utf-8 -*-
# Generated by Django 4.1.1 on 2022-10-19 16:46

from django.db import migrations
import pgtrigger.migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monta_user', '0015_remove_montauser_stops_protect_redundant_updates_and_more'),
    ]

    operations = [
        pgtrigger.migrations.RemoveTrigger(
            model_name='montauser',
            name='stops_protect_redundant_updates',
        ),
    ]
