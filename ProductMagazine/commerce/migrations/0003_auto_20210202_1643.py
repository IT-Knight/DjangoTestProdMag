# Generated by Django 3.1.5 on 2021-02-02 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0002_product_wishlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slu',
            field=models.CharField(max_length=8, unique=True),
        ),
    ]
