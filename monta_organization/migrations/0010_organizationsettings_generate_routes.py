# -*- coding: utf-8 -*-
# Generated by Django 4.1.1 on 2022-10-02 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("monta_organization", "0009_organizationsettings_traffic_model"),
    ]

    operations = [
        migrations.AddField(
            model_name="organizationsettings",
            name="generate_routes",
            field=models.BooleanField(
                default=False,
                help_text="Generate routes for the organization",
                verbose_name="Generate Routes",
            ),
        ),
    ]
