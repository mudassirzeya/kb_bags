# Generated by Django 4.2.13 on 2024-05-07 23:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfile",
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
                    "is_super_admin",
                    models.BooleanField(blank=True, default=False, null=True),
                ),
                ("is_staff", models.BooleanField(blank=True, default=False, null=True)),
                ("phone", models.CharField(blank=True, max_length=20, null=True)),
                (
                    "user_status",
                    models.CharField(
                        blank=True,
                        choices=[("Active", "Active"), ("InActive", "InActive")],
                        max_length=200,
                        null=True,
                    ),
                ),
                ("date_of_joining", models.DateTimeField(auto_now_add=True, null=True)),
                (
                    "user",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SalesEntryData",
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
                ("product_name", models.TextField(blank=True, null=True)),
                (
                    "product_quantity",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                (
                    "product_price",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                (
                    "product_image",
                    models.FileField(blank=True, null=True, upload_to="media"),
                ),
                ("added_date", models.DateTimeField(auto_now_add=True, null=True)),
                (
                    "staff",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="sales_entry.userprofile",
                    ),
                ),
            ],
        ),
    ]
