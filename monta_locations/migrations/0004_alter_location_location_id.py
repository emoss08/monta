# -*- coding: utf-8 -*-
# Generated by Django 4.1.1 on 2022-09-26 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("monta_locations", "0003_alter_location_address_line_1_alter_location_city"),
    ]

    operations = [
        migrations.AlterField(
            model_name="location",
            name="location_id",
            field=models.SlugField(
                blank=True,
                help_text="Unique ID for this location.",
                max_length=255,
                null=True,
                unique=True,
                verbose_name="Location ID",
            ),
        ),
    ]
