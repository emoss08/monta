# -*- coding: utf-8 -*-
# Generated by Django 4.1.1 on 2022-09-23 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("monta_order", "0004_alter_stop_destination_appointment_time_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="stop",
            name="destination_appointment_time",
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name="stop",
            name="origin_appointment_time",
            field=models.DateTimeField(),
        ),
    ]
