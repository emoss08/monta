# -*- coding: utf-8 -*-
# Generated by Django 4.1.1 on 2022-09-26 03:11

from django.db import migrations
import localflavor.us.models


class Migration(migrations.Migration):

    dependencies = [
        ("monta_equipment", "0004_equipment_vehicle_license_expiration"),
    ]

    operations = [
        migrations.AlterField(
            model_name="equipment",
            name="state",
            field=localflavor.us.models.USStateField(
                help_text="State of the vehicle", max_length=2, verbose_name="State"
            ),
        ),
    ]
