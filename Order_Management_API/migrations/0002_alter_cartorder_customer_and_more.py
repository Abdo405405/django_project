# Generated by Django 5.0.2 on 2024-03-23 08:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0001_initial'),
        ('Order_Management_API', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartorder',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Accounts.customer'),
        ),
        migrations.AlterField(
            model_name='cartorder',
            name='shipping_address',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='Accounts.address'),
        ),
    ]
