# -*- coding: utf-8 -*-
# Generated by Django 4.1.1 on 2022-09-26 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("monta_order", "0009_commodity_order_commodity_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="rate",
        ),
        migrations.AlterField(
            model_name="order",
            name="comment",
            field=models.TextField(
                blank=True, null=True, verbose_name="Planning Comment"
            ),
        ),
    ]
