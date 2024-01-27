# Generated by Django 4.2.8 on 2024-01-27 09:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("waffleAuth", "0002_alter_waffleuser_email"),
    ]

    operations = [
        migrations.AlterField(
            model_name="waffleuser",
            name="background_photo",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to="background_photos/<built-in function id>/",
            ),
        ),
        migrations.AlterField(
            model_name="waffleuser",
            name="nickname",
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name="waffleuser",
            name="profile_photo",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to="profile_photos/<built-in function id>/",
            ),
        ),
    ]
