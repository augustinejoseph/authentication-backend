# Generated by Django 4.2.11 on 2024-03-23 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BaseModel",
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
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="User",
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
                ("email", models.EmailField(max_length=254)),
                ("phone_number", models.CharField(max_length=15)),
                ("password", models.CharField(max_length=20)),
                ("is_delete", models.BooleanField(default=False)),
                ("is_verified", models.BooleanField(default=False)),
                ("logged_out", models.BooleanField(default=False)),
                ("last_login", models.DateTimeField(auto_now=True)),
                (
                    "last_device",
                    models.IntegerField(
                        blank=True,
                        choices=[
                            (1, "Android Phone"),
                            (2, "Laptop"),
                            (3, "i Phone"),
                            (4, "i Pad"),
                            (5, "Android Tab"),
                            (6, "TV"),
                            (7, "Other"),
                        ],
                        null=True,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
