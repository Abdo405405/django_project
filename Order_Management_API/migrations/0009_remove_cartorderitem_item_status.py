# Generated by Django 5.0.2 on 2024-06-22 19:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Order_Management_API', '0008_rename_item_cartorderitem_product_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartorderitem',
            name='item_status',
        ),
    ]
