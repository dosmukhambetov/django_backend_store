# Generated by Django 4.2.1 on 2023-05-31 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_basket'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stripe_product_price_id',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Stripe ID цены товара'),
        ),
    ]
