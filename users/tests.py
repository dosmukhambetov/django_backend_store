from datetime import timedelta
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from users.models import EmailVerification, User


class UserRegistrationViewTestCase(TestCase):

    def setUp(self) -> None:
        self.path = reverse('users:registration')
        self.data = {
            'first_name': 'TestName', 'last_name': 'TestLastName',
            'username': 'TestUsername', 'email': 'testmail@test.com',
            'password1': 'my_test_pass12345', 'password2': 'my_test_pass12345',
        }

    def test_user_registration_get(self):
        response = self.client.get(path=self.path)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(response.context_data['title'], 'Store - Регистрация')
        self.assertTemplateUsed(response, 'users/register.html')

    def test_user_registration_post_success(self):
        response = self.client.post(path=self.path, data=self.data)

        # check creating of user
        username = self.data['username']
        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(username=username).exists())

        # check creating of email verification
        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verification.exists())
        self.assertEquals(
            email_verification.first().expiration.date(),
            (now() + timedelta(hours=12)).date()
        )

    def test_user_registration_post_error(self):
        User.objects.create(username=self.data['username'])
        response = self.client.post(path=self.path, data=self.data)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует.', html=True)


class UserLoginViewTestCase(TestCase):

    def setUp(self) -> None:
        self.path = reverse('users:login')
        self.data = {
            'username': 'TestUsername',
            'password': 'my_test_pass12345'
        }

    def test_user_login_get(self):
        response = self.client.get(path=self.path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(response.context_data['title'], 'Store - Авторизация')
        self.assertTemplateUsed(response, 'users/login.html')

    def test_user_login_post_success(self):
        User.objects.create(username=self.data['username'], password=self.data['password'])
        response = self.client.post(path=self.path, data=self.data)
        username, password = self.data['username'], self.data['password']

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTrue(User.objects.filter(username=username, password=password).exists())

    def test_user_login_post_error(self):
        User.objects.create(username=self.data['username'], password=self.data['password'])
        response = self.client.post(path=self.path, data=self.data)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пожалуйста, введите правильные имя пользователя и пароль. '
                                      'Оба поля могут быть чувствительны к регистру.', html=True)
