# -*- coding: utf-8 -*-
# Generated by Django 4.1.1 on 2022-09-28 02:37

import localflavor.us.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("monta_user", "0004_remove_montauser_is_active"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="state",
            field=localflavor.us.models.USStateField(
                help_text="Enter the state of the user",
                max_length=2,
                verbose_name="State",
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="zip_code",
            field=localflavor.us.models.USZipCodeField(
                help_text="Enter the zip code of the user",
                max_length=10,
                verbose_name="Zip Code",
            ),
        ),
    ]
