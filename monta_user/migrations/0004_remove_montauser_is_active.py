# -*- coding: utf-8 -*-
# Generated by Django 4.1.1 on 2022-09-22 04:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("monta_user", "0003_remove_organization_org_timezone"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="montauser",
            name="is_active",
        ),
    ]
