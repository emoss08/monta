# -*- coding: utf-8 -*-
# Generated by Django 4.1.1 on 2022-09-26 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("monta_locations", "0002_alter_location_state_alter_location_zip_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="location",
            name="address_line_1",
            field=models.CharField(
                default=1,
                help_text="Address Line 1",
                max_length=255,
                verbose_name="Address Line 1",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="location",
            name="city",
            field=models.CharField(
                default=1, help_text="City", max_length=255, verbose_name="City"
            ),
            preserve_default=False,
        ),
    ]
