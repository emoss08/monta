# -*- coding: utf-8 -*-
# Generated by Django 4.1.1 on 2022-10-02 23:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("monta_user", "0005_alter_profile_state_alter_profile_zip_code"),
        ("monta_locations", "0005_alter_location_latitude_alter_location_longitude"),
    ]

    operations = [
        migrations.AlterField(
            model_name="location",
            name="organization",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="locations",
                related_query_name="location",
                to="monta_user.organization",
                verbose_name="Organization",
            ),
        ),
    ]
