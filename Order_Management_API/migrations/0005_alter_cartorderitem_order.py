# Generated by Django 5.0.2 on 2024-05-07 17:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order_Management_API', '0004_rename_order_qty_cartorderitem_qty_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartorderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='Order_Management_API.cartorder'),
        ),
    ]
