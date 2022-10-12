# -*- coding: utf-8 -*-
# Generated by Django 4.1.1 on 2022-10-02 23:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("monta_user", "0005_alter_profile_state_alter_profile_zip_code"),
        ("monta_hazardous_material", "0002_alter_hazardousclass_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hazardousclass",
            name="organization",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="hazardous_classes",
                related_query_name="hazardous_class",
                to="monta_user.organization",
            ),
        ),
    ]
