# -*- coding: utf-8 -*-
# Generated by Django 4.1.1 on 2022-10-02 23:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("monta_user", "0005_alter_profile_state_alter_profile_zip_code"),
        ("monta_customer", "0012_rename_is_primary_customercontact_primary_contact"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customerbillingprofile",
            name="organization",
            field=models.ForeignKey(
                help_text="Organization",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="billing_profiles",
                related_query_name="billing_profile",
                to="monta_user.organization",
                verbose_name="Organization",
            ),
        ),
        migrations.AlterField(
            model_name="customercontact",
            name="organization",
            field=models.ForeignKey(
                help_text="Organization",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="contacts",
                related_query_name="contact",
                to="monta_user.organization",
                verbose_name="Organization",
            ),
        ),
    ]
