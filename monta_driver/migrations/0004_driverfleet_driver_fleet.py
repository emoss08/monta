# -*- coding: utf-8 -*-
# Generated by Django 4.1.1 on 2022-09-12 21:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("monta_driver", "0003_fleet_fleet_monta_drive_name_f9f353_idx"),
    ]

    operations = [
        migrations.CreateModel(
            name="DriverFleet",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "driver",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="monta_driver.driver",
                    ),
                ),
                (
                    "fleet",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="monta_driver.fleet",
                    ),
                ),
            ],
            options={
                "verbose_name": "Driver Fleet",
                "verbose_name_plural": "Driver Fleets",
                "ordering": ["driver", "fleet"],
            },
        ),
        migrations.AddField(
            model_name="driver",
            name="fleet",
            field=models.ManyToManyField(
                related_name="drivers",
                through="monta_driver.DriverFleet",
                to="monta_driver.fleet",
            ),
        ),
    ]
