import stripe
from django.conf import settings
from django.db import models

from users.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY


class Category(models.Model):
    name = models.CharField(verbose_name='Название', max_length=128, unique=True)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)

    def __str__(self):
        return f"Категория: {self.name}"

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'category'
        ordering = ['name']


class Product(models.Model):
    name = models.CharField(verbose_name='Название', max_length=258)
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(verbose_name='Цена', max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(verbose_name='Количество', default=0)
    image = models.ImageField(verbose_name='Изображение', upload_to='products_images')
    stripe_product_price_id = models.CharField(verbose_name='Stripe ID цены товара', max_length=512, null=True,
                                               blank=True)
    category = models.ForeignKey(verbose_name='Категория', to=Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        db_table = 'products'
        ordering = ['name']

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.stripe_product_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_product_price_id = stripe_product_price['id']
        super(Product, self).save(force_insert=False, force_update=False, using=None, update_fields=None)

    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'], unit_amount=round(self.price * 100), currency='rub')
        return stripe_product_price


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)

    def stripe_products(self):
        line_items = []
        for basket in self:
            item = {
                'price': basket.product.stripe_product_price_id,
                'quantity': basket.quantity,
            }
            line_items.append(item)
        return line_items


class Basket(models.Model):
    user = models.ForeignKey(verbose_name='Пользователь', to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(verbose_name='Продукт', to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество', default=0)
    created_timestamp = models.DateTimeField(verbose_name='Время создания', auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f"Корзина для {self.user.username} | Продукт: {self.product.name}"

    def sum(self):
        return self.product.price * self.quantity

    def de_json(self):
        basket_item = {
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'sum': float(self.sum()),
        }
        return basket_item

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        db_table = 'basket'
        ordering = ['created_timestamp']
