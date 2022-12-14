# -*- coding: utf-8 -*-
# Generated by Django 4.1.1 on 2022-09-17 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("monta_driver", "0011_alter_driverfleet_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="driver",
            name="fleet",
            field=models.ManyToManyField(
                related_name="fleet_driver",
                through="monta_driver.DriverFleet",
                to="monta_driver.fleet",
            ),
        ),
    ]
