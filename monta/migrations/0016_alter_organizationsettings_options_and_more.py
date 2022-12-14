# -*- coding: utf-8 -*-
# Generated by Django 4.1.1 on 2022-09-19 00:02

import django.utils.timezone
import django_extensions.db.fields
import localflavor.us.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("monta", "0015_alter_documentclassification_organization_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="organizationsettings",
            options={"get_latest_by": "modified"},
        ),
        migrations.RemoveField(
            model_name="documentclassification",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="documentclassification",
            name="updated_at",
        ),
        migrations.RemoveField(
            model_name="location",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="location",
            name="updated_at",
        ),
        migrations.RemoveField(
            model_name="locationcontact",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="locationcontact",
            name="updated_at",
        ),
        migrations.RemoveField(
            model_name="organizationsettings",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="organizationsettings",
            name="updated_at",
        ),
        migrations.AddField(
            model_name="documentclassification",
            name="created",
            field=django_extensions.db.fields.CreationDateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="created",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="documentclassification",
            name="modified",
            field=django_extensions.db.fields.ModificationDateTimeField(
                auto_now=True, verbose_name="modified"
            ),
        ),
        migrations.AddField(
            model_name="location",
            name="created",
            field=django_extensions.db.fields.CreationDateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="created",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="location",
            name="modified",
            field=django_extensions.db.fields.ModificationDateTimeField(
                auto_now=True, verbose_name="modified"
            ),
        ),
        migrations.AddField(
            model_name="locationcontact",
            name="created",
            field=django_extensions.db.fields.CreationDateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="created",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="locationcontact",
            name="modified",
            field=django_extensions.db.fields.ModificationDateTimeField(
                auto_now=True, verbose_name="modified"
            ),
        ),
        migrations.AddField(
            model_name="organizationsettings",
            name="created",
            field=django_extensions.db.fields.CreationDateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="created",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="organizationsettings",
            name="modified",
            field=django_extensions.db.fields.ModificationDateTimeField(
                auto_now=True, verbose_name="modified"
            ),
        ),
        migrations.AlterField(
            model_name="documentclassification",
            name="description",
            field=models.TextField(blank=True, null=True, verbose_name="Description"),
        ),
        migrations.AlterField(
            model_name="documentclassification",
            name="name",
            field=models.CharField(max_length=255, unique=True, verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="location",
            name="address_line_1",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="Address Line 1"
            ),
        ),
        migrations.AlterField(
            model_name="location",
            name="address_line_2",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="Address Line 2"
            ),
        ),
        migrations.AlterField(
            model_name="location",
            name="city",
            field=models.CharField(
                blank=True,
                help_text="City",
                max_length=100,
                null=True,
                verbose_name="City",
            ),
        ),
        migrations.AlterField(
            model_name="location",
            name="description",
            field=models.TextField(
                blank=True, null=True, verbose_name="Location Description"
            ),
        ),
        migrations.AlterField(
            model_name="location",
            name="location_id",
            field=models.CharField(
                blank=True,
                max_length=10,
                null=True,
                unique=True,
                verbose_name="Location ID",
            ),
        ),
        migrations.AlterField(
            model_name="location",
            name="location_slug",
            field=models.SlugField(
                blank=True,
                max_length=255,
                null=True,
                unique=True,
                verbose_name="Location Slug",
            ),
        ),
        migrations.AlterField(
            model_name="location",
            name="name",
            field=models.CharField(
                max_length=255, unique=True, verbose_name="Location Name"
            ),
        ),
        migrations.AlterField(
            model_name="location",
            name="state",
            field=localflavor.us.models.USStateField(default=1, max_length=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="location",
            name="zip_code",
            field=localflavor.us.models.USZipCodeField(default=1, max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="locationcontact",
            name="contact_email",
            field=models.EmailField(
                blank=True, max_length=255, null=True, verbose_name="Contact Email"
            ),
        ),
        migrations.AlterField(
            model_name="locationcontact",
            name="contact_name",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="Contact Name"
            ),
        ),
        migrations.AlterField(
            model_name="locationcontact",
            name="contact_phone",
            field=models.CharField(
                blank=True,
                help_text="Phone",
                max_length=10,
                null=True,
                verbose_name="Contact Phone",
            ),
        ),
        migrations.AlterField(
            model_name="locationcontact",
            name="is_primary",
            field=models.BooleanField(default=False, verbose_name="Is Primary"),
        ),
    ]
