from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus

from message.models import Message

User = get_user_model()


class MessageViewTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_username')

        self.message_1 = Message.objects.create(text='Hello, it\'s my message', author=self.user)
        self.message_2 = Message.objects.create(text='Test text', author=self.user)
        self.message_3 = Message.objects.create(text='Just Hello', author=self.user)

    def test_home_page(self):
        path = reverse('home')
        response = self.client.get(path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'home.html')

    def test_create(self):
        path = reverse('home')

        data = {
            'text': 'Test new text',
            'author': self.user.id
        }

        self.client.force_login(self.user)

        response = self.client.post(path, data=data)

        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('home'))
        self.assertEquals(data['text'], Message.objects.last().text)
        self.assertEquals(data['author'], Message.objects.last().author.id)

    def test_update_page(self):
        path = reverse('message_update', args=(self.message_2.id,))
        response = self.client.get(path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'update.html')

    def test_update(self):
        path = reverse('message_update', args=(self.message_2.id,))

        data = {
            'text': 'Test another text',
            'author': self.user.id
        }

        self.client.force_login(self.user)

        response = self.client.post(path, data=data)
        self.message_2.refresh_from_db()

        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('home'))
        self.assertEquals('Test another text', self.message_2.text)

    def test_delete(self):
        path = reverse('message_delete', args=(self.message_2.id,))

        self.client.force_login(self.user)

        response = self.client.post(path)

        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('home'))
        self.assertEquals(Message.objects.all().count(), 2)
