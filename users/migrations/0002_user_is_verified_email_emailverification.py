# Generated by Django 4.2.1 on 2023-05-19 08:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_verified_email',
            field=models.BooleanField(default=False, verbose_name='Подтверждение почты'),
        ),
        migrations.CreateModel(
            name='EmailVerification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.UUIDField(unique=True, verbose_name='Идентификатор')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('expiration', models.DateTimeField(verbose_name='Время истечения')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Верификация почты',
                'verbose_name_plural': 'Верификации почты',
                'db_table': 'email_verification',
                'ordering': ['-created_at'],
            },
        ),
    ]