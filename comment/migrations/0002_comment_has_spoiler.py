# Generated by Django 4.2.8 on 2024-01-16 14:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("comment", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="has_spoiler",
            field=models.BooleanField(default=False),
        ),
    ]
