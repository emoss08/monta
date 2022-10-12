# -*- coding: utf-8 -*-
# Generated by Django 4.1.1 on 2022-09-27 04:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("monta_user", "0004_remove_montauser_is_active"),
        ("monta_customer", "0008_customerbillingprofile_document_class_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customerbillingprofile",
            name="customer",
            field=models.ForeignKey(
                help_text="Customer",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="billing_profiles",
                related_query_name="billing_profile",
                to="monta_customer.customer",
                verbose_name="Customer",
            ),
        ),
        migrations.AlterField(
            model_name="customerbillingprofile",
            name="document_class",
            field=models.ManyToManyField(
                help_text="Required Document Classifications",
                related_name="billing_profiles",
                related_query_name="billing_profile",
                to="monta_customer.documentclassification",
                verbose_name="Document Classifications",
            ),
        ),
        migrations.AlterField(
            model_name="customerbillingprofile",
            name="name",
            field=models.CharField(
                help_text="Name", max_length=255, unique=True, verbose_name="Name"
            ),
        ),
        migrations.AlterField(
            model_name="customerbillingprofile",
            name="organization",
            field=models.ForeignKey(
                help_text="Organization",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="customer_billing_profiles",
                related_query_name="customer_billing_profile",
                to="monta_user.organization",
                verbose_name="Organization",
            ),
        ),
    ]
