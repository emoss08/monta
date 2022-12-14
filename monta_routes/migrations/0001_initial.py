# -*- coding: utf-8 -*-
# Generated by Django 4.1.1 on 2022-09-30 00:12

import django.db.models.deletion
import django_extensions.db.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("monta_user", "0005_alter_profile_state_alter_profile_zip_code"),
    ]

    operations = [
        migrations.CreateModel(
            name="Route",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                (
                    "origin",
                    models.CharField(
                        blank=True,
                        help_text="Origin of the route",
                        max_length=255,
                        null=True,
                        verbose_name="Origin",
                    ),
                ),
                (
                    "destination",
                    models.CharField(
                        blank=True,
                        help_text="Destination",
                        max_length=255,
                        null=True,
                        verbose_name="Destination",
                    ),
                ),
                (
                    "mileage",
                    models.PositiveIntegerField(
                        blank=True,
                        help_text="Mileage",
                        null=True,
                        verbose_name="Mileage",
                    ),
                ),
                (
                    "duration",
                    models.DurationField(
                        blank=True,
                        help_text="Duration in seconds",
                        null=True,
                        verbose_name="Duration",
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        help_text="Organization",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="routes",
                        to="monta_user.organization",
                        verbose_name="Organization",
                    ),
                ),
            ],
            options={
                "verbose_name": "Route",
                "verbose_name_plural": "Routes",
                "ordering": ["-created"],
            },
        ),
        migrations.AddIndex(
            model_name="route",
            index=models.Index(
                fields=["-created"], name="monta_route_created_46f621_idx"
            ),
        ),
    ]
