# -*- coding: utf-8 -*-
# Generated by Django 4.1.1 on 2022-10-04 19:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("monta_fleet", "0001_initial"),
        ("monta_user", "0005_alter_profile_state_alter_profile_zip_code"),
        ("monta_driver", "0030_alter_drivercomment_comment_type_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="driver",
            name="fleet",
            field=models.ManyToManyField(
                blank=True,
                related_name="drivers",
                related_query_name="driver",
                to="monta_fleet.fleet",
                verbose_name="Fleet",
            ),
        ),
        migrations.AlterField(
            model_name="driver",
            name="organization",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="drivers",
                related_query_name="driver",
                to="monta_user.organization",
                verbose_name="Organization",
            ),
        ),
    ]
