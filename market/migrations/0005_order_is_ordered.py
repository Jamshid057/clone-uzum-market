# Generated by Django 5.2.1 on 2025-06-21 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("market", "0004_remove_order_is_ordered_order_address_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="is_ordered",
            field=models.BooleanField(default=False),
        ),
    ]
