# Generated by Django 4.2.8 on 2024-01-20 19:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0004_alter_role_options"),
    ]

    operations = [
        migrations.CreateModel(
            name="Carousel",
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
                ("title", models.CharField(max_length=50)),
                (
                    "movies",
                    models.ManyToManyField(
                        blank=True, related_name="carousels", to="content.movie"
                    ),
                ),
            ],
        ),
    ]
