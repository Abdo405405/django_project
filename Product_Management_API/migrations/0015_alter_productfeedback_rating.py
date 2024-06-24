# Generated by Django 5.0.2 on 2024-03-23 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product_Management_API', '0014_product_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productfeedback',
            name='rating',
            field=models.IntegerField(blank=True, choices=[(1, '★☆☆☆☆'), (2, '★★☆☆☆'), (3, '★★★☆☆'), (4, '★★★★☆'), (5, '★★★★★')], default=None, null=True),
        ),
    ]
