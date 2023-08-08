from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus

User = get_user_model()


class RegistrationViewTestCase(TestCase):

    def setUp(self):
        self.data = {
            'username': 'Name',
            'password1': '7ybv6j2lSe',
            'password2': '7ybv6j2lSe'
        }

        self.path = reverse('register')

    def test_users_registration_get(self):
        response = self.client.get(self.path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_users_registration_post(self):
        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username).exists())

        response = self.client.post(self.path, data=self.data)

        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(User.objects.filter(username=username).exists())