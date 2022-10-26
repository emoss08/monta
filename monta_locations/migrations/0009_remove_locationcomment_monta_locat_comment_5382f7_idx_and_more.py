# Generated by Django 4.1.2 on 2022-10-26 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("monta_locations", "0008_locationcontact_organization"),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name="locationcomment",
            name="monta_locat_comment_5382f7_idx",
        ),
        migrations.AddIndex(
            model_name="locationcomment",
            index=models.Index(
                fields=["comment"], name="monta_locat_comment_0ce199_idx"
            ),
        ),
    ]