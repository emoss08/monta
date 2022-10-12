# -*- coding: utf-8 -*-
# Generated by Django 4.1.1 on 2022-09-17 03:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("monta_driver", "0014_alter_driver_fleet"),
    ]

    operations = [
        migrations.AlterField(
            model_name="driver",
            name="fleet",
            field=models.ManyToManyField(
                related_name="driver_fleet",
                through="monta_driver.DriverFleet",
                to="monta_driver.fleet",
            ),
        ),
        migrations.AlterField(
            model_name="driverfleet",
            name="driver",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="assigned_driver",
                to="monta_driver.driver",
            ),
        ),
        migrations.AlterField(
            model_name="driverfleet",
            name="fleet",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="fleet",
                to="monta_driver.fleet",
            ),
        ),
    ]
