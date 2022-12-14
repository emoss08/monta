# -*- coding: utf-8 -*-
# Generated by Django 4.1.2 on 2022-10-20 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("monta_customer", "0015_alter_customerbillingprofile_customer"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customercontact",
            name="primary_contact",
        ),
        migrations.AddField(
            model_name="customercontact",
            name="is_billing",
            field=models.BooleanField(
                default=False,
                help_text="Is this the billing contact?",
                verbose_name="Is Billing",
            ),
        ),
        migrations.AddField(
            model_name="customercontact",
            name="is_primary",
            field=models.BooleanField(
                default=False,
                help_text="Is this the primary contact?",
                verbose_name="Is Primary",
            ),
        ),
    ]
