# -*- coding: utf-8 -*-
# Generated by Django 4.1.1 on 2022-09-29 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("monta_billing", "0009_billinghistory_sub_total"),
    ]

    operations = [
        migrations.AddField(
            model_name="billingqueue",
            name="sub_total",
            field=models.DecimalField(
                decimal_places=2, default=1, max_digits=10, verbose_name="Sub Total"
            ),
            preserve_default=False,
        ),
    ]
