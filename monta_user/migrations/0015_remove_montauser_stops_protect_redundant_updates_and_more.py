# Generated by Django 4.1.1 on 2022-10-19 16:45

from django.db import migrations
import pgtrigger.compiler
import pgtrigger.migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monta_user', '0014_remove_montauser_stops_protect_redundant_updates_and_more'),
    ]

    operations = [
        pgtrigger.migrations.RemoveTrigger(
            model_name='montauser',
            name='stops_protect_redundant_updates',
        ),
        pgtrigger.migrations.AddTrigger(
            model_name='montauser',
            trigger=pgtrigger.compiler.Trigger(name='stops_protect_redundant_updates', sql=pgtrigger.compiler.UpsertTriggerSql(condition='WHEN (OLD.* IS DISTINCT FROM NEW.*)', func="RAISE EXCEPTION 'pgtrigger: Cannot update rows from % table', TG_TABLE_NAME;", hash='4ccfd502176d6b4586835b8dfd24b89095f5ebba', operation='UPDATE', pgid='pgtrigger_stops_protect_redundant_updates_ea400', table='monta_user_montauser', when='BEFORE')),
        ),
    ]
