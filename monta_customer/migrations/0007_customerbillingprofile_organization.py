# -*- coding: utf-8 -*-
# Generated by Django 4.1.1 on 2022-09-27 04:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("monta_user", "0004_remove_montauser_is_active"),
        ("monta_customer", "0006_customerbillingprofile_customer_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="customerbillingprofile",
            name="organization",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="customer_billing_profiles",
                related_query_name="customer_billing_profile",
                to="monta_user.organization",
            ),
            preserve_default=False,
        ),
    ]
