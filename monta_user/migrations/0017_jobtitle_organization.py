# -*- coding: utf-8 -*-
# Generated by Django 4.1.2 on 2022-10-20 04:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("monta_user", "0016_remove_montauser_stops_protect_redundant_updates"),
    ]

    operations = [
        migrations.AddField(
            model_name="jobtitle",
            name="organization",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="job_titles",
                to="monta_user.organization",
            ),
            preserve_default=False,
        ),
    ]
