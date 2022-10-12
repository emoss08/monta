# -*- coding: utf-8 -*-
# Generated by Django 4.1.1 on 2022-09-17 03:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        (
            "monta_driver",
            "0009_alter_driver_options_alter_driverprofile_options_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="driverfleet",
            name="driver",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="driver_fleet",
                to="monta_driver.driver",
            ),
        ),
    ]
