# -*- coding: utf-8 -*-
# Generated by Django 4.1.1 on 2022-09-27 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("monta_billing", "0003_additionalcharge_unit"),
    ]

    operations = [
        migrations.AddField(
            model_name="additionalcharge",
            name="total_amount",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text="Total amount of the additional charge",
                max_digits=10,
                null=True,
                verbose_name="Total Amount",
            ),
        ),
    ]
