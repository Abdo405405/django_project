# Generated by Django 5.0.2 on 2024-03-01 07:22

import django.db.models.deletion
import shortuuid.django_fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisement_Board',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, upload_to='advertisement_images/')),
                ('link', models.URLField(blank=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('priority', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Advertisement Board',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('country_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('contact', models.CharField(max_length=15)),
                ('unit_number', models.IntegerField()),
                ('street_number', models.IntegerField()),
                ('address_line1', models.CharField(max_length=200)),
                ('address_line2', models.CharField(blank=True, max_length=200)),
                ('city', models.CharField(max_length=100)),
                ('region', models.CharField(max_length=100)),
                ('postal_code', models.IntegerField(blank=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.country')),
            ],
            options={
                'verbose_name': 'Address',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(blank=True, upload_to='Customers')),
                ('date_of_birth', models.DateField(default='2002-01-22')),
                ('addresses', models.ManyToManyField(to='core.address')),
                ('default_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='default_for_customer', to='core.address')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Customer',
            },
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('vid', shortuuid.django_fields.ShortUUIDField(alphabet='0123456789', length=10, max_length=20, prefix='vend', unique=True)),
                ('contact', models.CharField(max_length=15)),
                ('image', models.ImageField(blank=True, upload_to='All Vendors')),
                ('description', models.TextField(blank=True, null=True)),
                ('chat_resp_time', models.CharField(default='100', max_length=100)),
                ('authentic_rating', models.CharField(max_length=100)),
                ('shipping_on_time', models.CharField(max_length=100)),
                ('address', models.ManyToManyField(to='core.address')),
                ('default_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='default_for_vendor', to='core.address')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Vendor',
            },
        ),
    ]
