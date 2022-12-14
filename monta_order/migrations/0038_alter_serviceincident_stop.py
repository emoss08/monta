# -*- coding: utf-8 -*-
# Generated by Django 4.1.1 on 2022-10-03 04:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("monta_order", "0037_alter_serviceincident_movement"),
    ]

    operations = [
        migrations.AlterField(
            model_name="serviceincident",
            name="stop",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="service_incidents",
                related_query_name="service_incident",
                to="monta_order.stop",
                verbose_name="Stop",
            ),
        ),
    ]
