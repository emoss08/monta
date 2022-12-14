# -*- coding: utf-8 -*-
# Generated by Django 4.1.1 on 2022-09-13 05:27

from datetime import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("monta_driver", "0007_remove_driverprofile_email_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="drivercontact",
            name="contact_name",
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="driverprofile",
            name="address_line_1",
            field=models.CharField(default=1, help_text="Address", max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="driverprofile",
            name="city",
            field=models.CharField(
                default=1, help_text="City of residence", max_length=100
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="driverprofile",
            name="license_expiration",
            field=models.DateField(
                default=datetime.now(), help_text="License Expiration"
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="driverprofile",
            name="license_state",
            field=models.CharField(default=1, help_text="License State", max_length=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="driverprofile",
            name="state",
            field=models.CharField(
                default=1, help_text="State of residence", max_length=2
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="driverprofile",
            name="zip_code",
            field=models.PositiveIntegerField(
                default=1, help_text="Zip Code / Postal Code"
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="driverqualification",
            name="description",
            field=models.TextField(
                blank=True, help_text="Description of Driver Qualification", null=True
            ),
        ),
        migrations.AlterField(
            model_name="driverqualification",
            name="dq_file",
            field=models.FileField(
                default=1,
                help_text="Qualification File",
                upload_to="drivers/qualification",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="driverqualification",
            name="name",
            field=models.CharField(
                default=1, help_text="Qualification Name", max_length=255
            ),
            preserve_default=False,
        ),
    ]
