# -*- coding: utf-8 -*-
# Generated by Django 4.1.1 on 2022-09-12 05:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("monta", "0013_remove_driver_organization_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="CommentType",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(blank=True, max_length=255, null=True)),
                ("description", models.TextField(blank=True, null=True)),
            ],
            options={
                "verbose_name": "Comment Type",
                "verbose_name_plural": "Comment Types",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Driver",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "driver_id",
                    models.CharField(blank=True, max_length=10, null=True, unique=True),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("first_name", models.CharField(max_length=255)),
                (
                    "middle_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("last_name", models.CharField(max_length=255)),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="monta.organization",
                    ),
                ),
            ],
            options={
                "verbose_name": "Driver",
                "verbose_name_plural": "Drivers",
                "ordering": ["first_name", "last_name"],
            },
        ),
        migrations.CreateModel(
            name="DriverQualification",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(blank=True, max_length=255, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "dq_file",
                    models.FileField(
                        blank=True, null=True, upload_to="drivers/qualification"
                    ),
                ),
                ("dq_file_size", models.PositiveIntegerField(blank=True, null=True)),
                (
                    "doc_class",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="monta.documentclassification",
                    ),
                ),
                (
                    "driver",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="monta_driver.driver",
                    ),
                ),
            ],
            options={
                "verbose_name": "Driver Qualification",
                "verbose_name_plural": "Driver Qualifications",
                "ordering": ["driver", "doc_class"],
            },
        ),
        migrations.CreateModel(
            name="DriverProfile",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "profile_picture",
                    models.ImageField(blank=True, null=True, upload_to="drivers/"),
                ),
                (
                    "address_line_1",
                    models.CharField(
                        blank=True, help_text="Address", max_length=255, null=True
                    ),
                ),
                (
                    "address_line_2",
                    models.CharField(
                        blank=True, help_text="Address", max_length=255, null=True
                    ),
                ),
                (
                    "city",
                    models.CharField(
                        blank=True, help_text="City", max_length=100, null=True
                    ),
                ),
                (
                    "state",
                    models.CharField(
                        blank=True, help_text="State", max_length=2, null=True
                    ),
                ),
                (
                    "zip_code",
                    models.PositiveIntegerField(blank=True, help_text="Zip", null=True),
                ),
                (
                    "phone",
                    models.CharField(
                        blank=True, help_text="Phone", max_length=10, null=True
                    ),
                ),
                ("email", models.EmailField(blank=True, max_length=255, null=True)),
                (
                    "license_number",
                    models.CharField(help_text="License Number", max_length=100),
                ),
                (
                    "license_state",
                    models.CharField(
                        blank=True, help_text="License State", max_length=2, null=True
                    ),
                ),
                (
                    "license_expiration",
                    models.DateField(
                        blank=True, help_text="License Expiration", null=True
                    ),
                ),
                ("is_hazmat", models.BooleanField(default=False, help_text="Hazmat")),
                ("is_tanker", models.BooleanField(default=False, help_text="Tanker")),
                (
                    "is_double_triple",
                    models.BooleanField(default=False, help_text="Double/Triples"),
                ),
                (
                    "is_passenger",
                    models.BooleanField(default=False, help_text="Passenger"),
                ),
                (
                    "driver",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="monta_driver.driver",
                    ),
                ),
            ],
            options={
                "verbose_name": "Driver Profile",
                "verbose_name_plural": "Driver Profiles",
                "ordering": ["driver"],
            },
        ),
        migrations.CreateModel(
            name="DriverContact",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "contact_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "contact_email",
                    models.EmailField(blank=True, max_length=255, null=True),
                ),
                (
                    "contact_phone",
                    models.CharField(
                        blank=True, help_text="Phone", max_length=10, null=True
                    ),
                ),
                (
                    "is_primary",
                    models.BooleanField(default=False, help_text="Primary Contact"),
                ),
                (
                    "is_emergency",
                    models.BooleanField(default=False, help_text="Emergency Contact"),
                ),
                (
                    "driver",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="monta_driver.driver",
                    ),
                ),
            ],
            options={
                "verbose_name": "Driver Contact",
                "verbose_name_plural": "Driver Contacts",
                "ordering": ["driver", "contact_name"],
            },
        ),
        migrations.CreateModel(
            name="DriverComment",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("comment", models.TextField(blank=True, null=True)),
                (
                    "comment_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="monta_driver.commenttype",
                    ),
                ),
                (
                    "driver",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="monta_driver.driver",
                    ),
                ),
            ],
            options={
                "verbose_name": "Driver Comment",
                "verbose_name_plural": "Driver Comments",
                "ordering": ["driver", "comment_type"],
            },
        ),
    ]
