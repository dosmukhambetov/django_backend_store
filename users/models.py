from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now


class User(AbstractUser):
    image = models.ImageField(verbose_name='Изображение', upload_to='users_images', null=True, blank=True)
    is_verified_email = models.BooleanField(verbose_name='Подтверждение почты', default=False)

    def __str__(self):
        return f"Пользователь: {self.username}"


class EmailVerification(models.Model):
    code = models.UUIDField(verbose_name='Идентификатор', unique=True)
    user = models.ForeignKey(verbose_name='Пользователь', to=User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name='Время создания', auto_now_add=True)
    expiration = models.DateTimeField(verbose_name='Время истечения')

    def __str__(self):
        return f"Верификация почты для пользователя {self.user.username}"

    def send_verification_email(self):
        link = reverse('users:email_verification', args=[self.user.email, self.code])
        verification_link = f"{settings.DOMAIN_NAME}{link}"
        subject = f"Подтверждение учетной записи для {self.user.username}"
        message = f"Для подтверждение учетной записи для {self.user.email} перейдите по ссылке {verification_link}"
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        return True if now() >= self.expiration else False

    class Meta:
        verbose_name = 'Верификация почты'
        verbose_name_plural = 'Верификации почты'
        db_table = 'email_verification'
        ordering = ['-created_at']
