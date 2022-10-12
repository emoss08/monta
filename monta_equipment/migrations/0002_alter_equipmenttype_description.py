# -*- coding: utf-8 -*-
# Generated by Django 4.1.1 on 2022-09-20 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("monta_equipment", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="equipmenttype",
            name="description",
            field=models.CharField(
                blank=True,
                max_length=200,
                null=True,
                verbose_name="Equipment Type Description",
            ),
        ),
    ]
