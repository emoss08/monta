# -*- coding: utf-8 -*-
# Generated by Django 4.1.2 on 2022-10-20 03:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monta_customer', '0014_customerbillingprofile_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerbillingprofile',
            name='customer',
            field=models.OneToOneField(help_text='Customer', on_delete=django.db.models.deletion.PROTECT, related_name='billing_profiles', related_query_name='billing_profile', to='monta_customer.customer', verbose_name='Customer'),
        ),
    ]
