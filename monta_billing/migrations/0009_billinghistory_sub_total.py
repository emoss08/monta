# -*- coding: utf-8 -*-
# Generated by Django 4.1.1 on 2022-09-29 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("monta_billing", "0008_billinghistory_bill_type_billingqueue_bill_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="billinghistory",
            name="sub_total",
            field=models.DecimalField(
                decimal_places=2, default=1, max_digits=10, verbose_name="Sub Total"
            ),
            preserve_default=False,
        ),
    ]
