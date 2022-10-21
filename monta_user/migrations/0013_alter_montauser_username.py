# -*- coding: utf-8 -*-
# Generated by Django 4.1.1 on 2022-10-19 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("monta_user", "0012_alter_montauser_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="montauser",
            name="username",
            field=models.CharField(
                help_text="Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.",
                max_length=30,
                unique=True,
                verbose_name="Username",
            ),
        ),
    ]
