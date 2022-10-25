# -*- coding: utf-8 -*-
# Generated by Django 4.1.1 on 2022-09-29 15:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("monta_user", "0005_alter_profile_state_alter_profile_zip_code"),
        ("monta_driver", "0027_driverhour_driverhour_monta_drive_driver__6188c9_idx"),
    ]

    operations = [
        migrations.AddField(
            model_name="drivercomment",
            name="organization",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="driver_comments",
                to="monta_user.organization",
                verbose_name="Organization",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="drivercomment",
            name="comment_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="comments",
                to="monta_driver.commenttype",
                verbose_name="Comment Type",
            ),
        ),
        migrations.AlterField(
            model_name="drivercomment",
            name="driver",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="driver_comments",
                to="monta_driver.driver",
                verbose_name="Driver",
            ),
        ),
    ]
