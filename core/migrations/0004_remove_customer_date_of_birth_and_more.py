# Generated by Django 5.0.2 on 2024-03-17 11:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_vendor_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='date_of_birth',
        ),
        migrations.AlterField(
            model_name='customer',
            name='addresses',
            field=models.ManyToManyField(blank=True, null=True, to='core.address'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
