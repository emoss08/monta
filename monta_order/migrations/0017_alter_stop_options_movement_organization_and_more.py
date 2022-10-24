# -*- coding: utf-8 -*-
# Generated by Django 4.1.1 on 2022-09-26 04:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("monta_user", "0004_remove_montauser_is_active"),
        ("monta_equipment", "0005_alter_equipment_state"),
        ("monta_driver", "0025_alter_driver_options"),
        ("monta_order", "0016_remove_order_entry_date_alter_movement_status_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="stop",
            options={
                "ordering": ["sequence"],
                "verbose_name": "Stop",
                "verbose_name_plural": "Stops",
            },
        ),
        migrations.AddField(
            model_name="movement",
            name="organization",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="movements",
                related_query_name="movement",
                to="monta_user.organization",
                verbose_name="Organization",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="movement",
            name="assigned_driver",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="movements",
                related_query_name="movement",
                to="monta_driver.driver",
                verbose_name="Assigned Driver",
            ),
        ),
        migrations.AlterField(
            model_name="movement",
            name="assigned_driver_2",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="movements_two",
                related_query_name="movement_two",
                to="monta_driver.driver",
                verbose_name="Assigned Driver 2",
            ),
        ),
        migrations.AlterField(
            model_name="movement",
            name="equipment",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="movements",
                related_query_name="movement",
                to="monta_equipment.equipment",
                verbose_name="Equipment",
            ),
        ),
        migrations.AlterField(
            model_name="movement",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="movements",
                related_query_name="movement",
                to="monta_order.order",
                verbose_name="Order",
            ),
        ),
        migrations.AddIndex(
            model_name="stop",
            index=models.Index(
                fields=["sequence"], name="monta_order_sequenc_79afce_idx"
            ),
        ),
    ]
