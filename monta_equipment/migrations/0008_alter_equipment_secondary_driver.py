# -*- coding: utf-8 -*-
# Generated by Django 4.1.1 on 2022-10-14 02:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("monta_driver", "0033_alter_driver_options"),
        ("monta_equipment", "0007_equipmentpermit_organization_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="equipment",
            name="secondary_driver",
            field=models.ForeignKey(
                blank=True,
                help_text="Secondary driver of the equipment.",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="equipments_secondary",
                related_query_name="equipment_secondary",
                to="monta_driver.driver",
                verbose_name="Secondary Driver",
            ),
        ),
    ]
