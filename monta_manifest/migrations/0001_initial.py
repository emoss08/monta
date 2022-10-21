# -*- coding: utf-8 -*-
# Generated by Django 4.1.2 on 2022-10-20 03:27

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("monta_user", "0016_remove_montauser_stops_protect_redundant_updates"),
        ("monta_order", "0043_stop_stops_protect_redundant_updates"),
    ]

    operations = [
        migrations.CreateModel(
            name="Manifest",
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
                    "manifest_number",
                    models.CharField(
                        max_length=255, unique=True, verbose_name="Manifest Number"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("AVAILABLE", "Available"),
                            ("IN_PROGRESS", "In Progress"),
                            ("COMPLETED", "Completed"),
                            ("CANCELLED", "Cancelled"),
                        ],
                        default="AVAILABLE",
                        max_length=20,
                        verbose_name="Status",
                    ),
                ),
                (
                    "orders",
                    models.ManyToManyField(
                        help_text="Orders to be included in the manifest.",
                        related_name="manifests",
                        related_query_name="manifest",
                        to="monta_order.order",
                        verbose_name="Orders",
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="manifests",
                        related_query_name="manifest",
                        to="monta_user.organization",
                        verbose_name="Organization",
                    ),
                ),
            ],
            options={
                "verbose_name": "Manifest",
                "verbose_name_plural": "Manifests",
                "ordering": ["-created"],
            },
        ),
    ]
