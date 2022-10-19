# -*- coding: utf-8 -*-
# Generated by Django 4.1.1 on 2022-10-19 14:54

from django.db import migrations
import pgtrigger.compiler
import pgtrigger.migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monta_order', '0042_order_bol_number_order_consignee_ref_num_and_more'),
    ]

    operations = [
        pgtrigger.migrations.AddTrigger(
            model_name='stop',
            trigger=pgtrigger.compiler.Trigger(name='stops_protect_redundant_updates', sql=pgtrigger.compiler.UpsertTriggerSql(condition='WHEN (OLD.* IS DISTINCT FROM NEW.*)', func="RAISE EXCEPTION 'pgtrigger: Cannot update rows from % table', TG_TABLE_NAME;", hash='bcb8c39cb02fbba498ac46cb97d93175e3d1afe1', operation='UPDATE', pgid='pgtrigger_stops_protect_redundant_updates_17c89', table='monta_order_stop', when='BEFORE')),
        ),
    ]
