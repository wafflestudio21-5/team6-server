# Generated by Django 4.2.8 on 2024-01-27 09:59

from django.db import migrations, models
import waffleAuth.models


class Migration(migrations.Migration):
    dependencies = [
        ("waffleAuth", "0003_alter_waffleuser_background_photo_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="waffleuser",
            name="background_photo",
            field=models.FileField(
                blank=True, null=True, upload_to=waffleAuth.models.background_photo_path
            ),
        ),
        migrations.AlterField(
            model_name="waffleuser",
            name="profile_photo",
            field=models.FileField(
                blank=True, null=True, upload_to=waffleAuth.models.profile_photo_path
            ),
        ),
    ]
