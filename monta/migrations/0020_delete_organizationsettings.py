# -*- coding: utf-8 -*-
# Generated by Django 4.1.1 on 2022-09-29 16:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("monta", "0019_delete_documentclassification"),
    ]

    operations = [
        migrations.DeleteModel(
            name="OrganizationSettings",
        ),
    ]
