# -*- coding: utf-8 -*-
# Generated by Django 4.1.1 on 2022-09-19 03:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("monta_driver", "0021_remove_commenttype_created_at_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="fleet",
            name="fleet_manager",
        ),
        migrations.RemoveField(
            model_name="fleet",
            name="organization",
        ),
    ]
