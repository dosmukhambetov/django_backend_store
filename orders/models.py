from django.db import models

from products.models import Basket
from users.models import User


class Order(models.Model):
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    STATUSES = (
        (CREATED, 'Создан'),
        (PAID, 'Оплачен'),
        (ON_WAY, 'В пути'),
        (DELIVERED, 'Доставлен'),
    )

    first_name = models.CharField(verbose_name='Имя', max_length=64)
    last_name = models.CharField(verbose_name='Фамилия', max_length=64)
    email = models.EmailField(verbose_name='Почта', max_length=256)
    address = models.CharField(verbose_name='Адрес доставки', max_length=256)
    basket_history = models.JSONField(verbose_name='Корзина', default=dict)
    created_at = models.DateTimeField(verbose_name='Время создания', auto_now_add=True)
    status = models.SmallIntegerField(verbose_name='Статус заказа', default=CREATED, choices=STATUSES)
    initiator = models.ForeignKey(verbose_name='Пользователь', to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Заказ #{self.id}. {self.first_name} {self.last_name}"

    def update_after_payment(self):
        baskets = Basket.objects.filter(user=self.initiator)
        self.status = self.PAID
        self.basket_history = {
            'purchased_items': [basket.de_json() for basket in baskets],
            'total_sum': float(baskets.total_sum()),
        }
        baskets.delete()
        self.save()

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        db_table = 'orders'
        ordering = ['-created_at']
