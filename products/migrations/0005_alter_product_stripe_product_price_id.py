# Generated by Django 4.2.1 on 2023-05-31 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_product_stripe_product_price_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='stripe_product_price_id',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='Stripe ID цены товара'),
        ),
    ]
