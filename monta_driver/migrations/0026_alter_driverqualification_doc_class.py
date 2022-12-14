# -*- coding: utf-8 -*-
# Generated by Django 4.1.1 on 2022-09-27 04:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("monta_customer", "0006_customerbillingprofile_customer_and_more"),
        ("monta_driver", "0025_alter_driver_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="driverqualification",
            name="doc_class",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="monta_customer.documentclassification",
            ),
        ),
    ]
