# -*- coding: utf-8 -*-
# Generated by Django 4.1.1 on 2022-09-23 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("monta_equipment", "0003_equipmentpermit_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="equipment",
            name="vehicle_license_expiration",
            field=models.DateField(
                blank=True, null=True, verbose_name="Vehicle License Expiration"
            ),
        ),
    ]
