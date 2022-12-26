# Generated by Django 4.1.3 on 2022-12-13 10:04

import accounts.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_delete_profile"),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
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
                    "sex",
                    models.CharField(blank=True, max_length=255, verbose_name="性别"),
                ),
                (
                    "introduction",
                    models.TextField(blank=True, max_length=1000, verbose_name="简介"),
                ),
                (
                    "photo",
                    models.ImageField(
                        blank=True,
                        upload_to=accounts.models.upload_to,
                        verbose_name="头像",
                    ),
                ),
                (
                    "cover",
                    models.ImageField(
                        blank=True,
                        upload_to=accounts.models.upload_to,
                        verbose_name="封面",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.customuser",
                        verbose_name="用户",
                    ),
                ),
            ],
            options={"verbose_name": "资料", "verbose_name_plural": "资料",},
        ),
    ]
