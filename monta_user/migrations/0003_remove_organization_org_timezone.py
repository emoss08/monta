# -*- coding: utf-8 -*-
# Generated by Django 4.1.1 on 2022-09-19 19:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "monta_user",
            "0002_alter_profile_options_remove_jobtitle_created_at_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="organization",
            name="org_timezone",
        ),
    ]
