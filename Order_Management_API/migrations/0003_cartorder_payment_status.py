# Generated by Django 5.0.2 on 2024-05-02 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order_Management_API', '0002_alter_cartorder_customer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartorder',
            name='payment_status',
            field=models.CharField(choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')], default='Unpaid', max_length=30),
        ),
    ]
