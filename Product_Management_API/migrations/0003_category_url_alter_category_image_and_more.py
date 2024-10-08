# Generated by Django 5.0.2 on 2024-03-03 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product_Management_API', '0002_remove_category_cid_alter_product_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='url',
            field=models.URLField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='Categories'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=255),
        ),
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(db_index=True, max_length=255),
        ),
    ]
