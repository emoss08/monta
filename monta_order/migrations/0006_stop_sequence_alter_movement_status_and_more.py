# -*- coding: utf-8 -*-
# Generated by Django 4.1.1 on 2022-09-23 00:30

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("monta_order", "0005_alter_stop_destination_appointment_time_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="stop",
            name="sequence",
            field=models.PositiveIntegerField(default=0, verbose_name="Sequence"),
        ),
        migrations.AlterField(
            model_name="movement",
            name="status",
            field=models.CharField(
                choices=[
                    ("AVAILABLE", "Available"),
                    ("IN_PROGRESS", "In Progress"),
                    ("COMPLETED", "Completed"),
                ],
                default="AVAILABLE",
                max_length=20,
                verbose_name="Entry Date",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="bill_date",
            field=models.DateField(blank=True, null=True, verbose_name="Billed Date"),
        ),
        migrations.AlterField(
            model_name="order",
            name="entry_date",
            field=models.DateTimeField(
                blank=True,
                default=django.utils.timezone.now,
                null=True,
                verbose_name="Entry Date",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="sub_total",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=10,
                null=True,
                verbose_name="Sub Total Amount",
            ),
        ),
    ]
