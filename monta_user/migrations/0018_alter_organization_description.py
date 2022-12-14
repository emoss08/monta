# Generated by Django 4.1.2 on 2022-10-26 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("monta_user", "0017_jobtitle_organization"),
    ]

    operations = [
        migrations.AlterField(
            model_name="organization",
            name="description",
            field=models.TextField(
                blank=True,
                help_text="The description of the organization",
                null=True,
                verbose_name="Organization Description",
            ),
        ),
    ]
