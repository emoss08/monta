# -*- coding: utf-8 -*-
# Generated by Django 4.1.1 on 2022-09-26 02:15

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ("monta_user", "0004_remove_montauser_is_active"),
        (
            "monta_organization",
            "0003_alter_googleapi_api_key_alter_googleapi_client_id_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="Integration",
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
                    "name",
                    models.CharField(
                        choices=[
                            ("google_maps", "Google Maps"),
                            ("google_places", "Google Places"),
                        ],
                        max_length=255,
                        verbose_name="Name",
                    ),
                ),
                (
                    "api_key",
                    models.CharField(
                        blank=True,
                        help_text="Google Maps API Key",
                        max_length=255,
                        null=True,
                        verbose_name="API Key",
                    ),
                ),
                (
                    "client_id",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="Client ID"
                    ),
                ),
                (
                    "client_secret",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="Client Secret",
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="google_api",
                        to="monta_user.organization",
                    ),
                ),
            ],
            options={
                "verbose_name": "Google Maps",
                "verbose_name_plural": "Google Maps",
                "ordering": ["name"],
            },
        ),
        migrations.DeleteModel(
            name="GoogleAPI",
        ),
        migrations.AddIndex(
            model_name="integration",
            index=models.Index(fields=["name"], name="monta_organ_name_b8bd21_idx"),
        ),
    ]
