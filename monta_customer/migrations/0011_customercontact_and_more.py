# -*- coding: utf-8 -*-
# Generated by Django 4.1.1 on 2022-09-27 22:20

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ("monta_user", "0004_remove_montauser_is_active"),
        ("monta_customer", "0010_alter_customerbillingprofile_options_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="CustomerContact",
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
                    "contact_name",
                    models.CharField(
                        help_text="Name", max_length=255, verbose_name="Name"
                    ),
                ),
                (
                    "contact_email",
                    models.EmailField(
                        help_text="Email", max_length=255, verbose_name="Email"
                    ),
                ),
                (
                    "contact_phone",
                    models.CharField(
                        blank=True,
                        help_text="Phone",
                        max_length=10,
                        null=True,
                        verbose_name="Phone",
                    ),
                ),
                (
                    "fax_number",
                    models.PositiveIntegerField(
                        blank=True,
                        help_text="Fax Number",
                        null=True,
                        verbose_name="Fax Number",
                    ),
                ),
                (
                    "is_primary",
                    models.BooleanField(default=False, verbose_name="Is Primary"),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        help_text="Customer",
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="contacts",
                        related_query_name="contact",
                        to="monta_customer.customer",
                        verbose_name="Customer",
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        help_text="Organization",
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="customer_contacts",
                        related_query_name="customer_contact",
                        to="monta_user.organization",
                        verbose_name="Organization",
                    ),
                ),
            ],
            options={
                "verbose_name": "Customer Contact",
                "verbose_name_plural": "Customer Contacts",
                "ordering": ["contact_name"],
            },
        ),
        migrations.AddIndex(
            model_name="customercontact",
            index=models.Index(
                fields=["contact_name"], name="monta_custo_contact_c953d4_idx"
            ),
        ),
    ]
