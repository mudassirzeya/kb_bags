# Generated by Django 4.2.13 on 2024-07-05 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sales_entry", "0004_salesentrydata_auto_added_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="salesentrydata",
            name="added_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]
