import json

from django.contrib.auth import get_user_model

from users.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from message.models import Message
from api.serializers import MessageSerializer

User = get_user_model()


class MessageApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')

        self.message_1 = Message.objects.create(text='Hello, it\'s my message', author=self.user)
        self.message_2 = Message.objects.create(text='Test text', author=self.user)
        self.message_3 = Message.objects.create(text='Just Hello', author=self.user)

    def test_get(self):
        url = reverse('message-list')
        response = self.client.get(url)
        serializer_data = MessageSerializer([self.message_1, self.message_2, self.message_3], many=True).data

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(serializer_data, response.data)

    def test_post(self):
        self.assertEquals(3, Message.objects.all().count())

        url = reverse('message-list')
        data = {
            'text': 'test text',
            'author': self.user.id
        }

        self.client.force_login(self.user)

        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')

        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        self.assertEquals(4, Message.objects.all().count())
        self.assertEquals(self.user, Message.objects.last().author)

    def test_put(self):
        url = reverse('message-detail', args=(self.message_2.id,))
        data = {
            'text': 'Test another text',
            'author': self.user.id
        }

        self.client.force_login(self.user)

        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.message_2.refresh_from_db()
        self.assertEquals('Test another text', self.message_2.text)

    def test_put_not_author(self):
        self.user2 = User.objects.create(username='test_username2')

        url = reverse('message-detail', args=(self.message_2.id,))
        data = {
            'text': 'Test another text',
        }

        self.client.force_login(self.user2)

        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')

        self.assertEquals(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEquals({'detail': ErrorDetail(string='You do not have permission to perform this action.',
                                                 code='permission_denied')},
                          response.data)
        self.message_2.refresh_from_db()
        self.assertEquals('Test text', self.message_2.text)

    def test_delete(self):
        self.assertEquals(3, Message.objects.all().count())

        url = reverse('message-detail', args=(self.message_1.id,))
        data = {
            'text': 'test text',
        }
        json_data = json.dumps(data)

        self.client.force_login(self.user)
        response = self.client.delete(url, data=json_data, content_type='application/json')

        self.assertEquals(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEquals(2, Message.objects.all().count())

    def test_delete_not_author(self):
        self.user2 = User.objects.create(username='test_username2')
        self.assertEquals(3, Message.objects.all().count())

        url = reverse('message-detail', args=(self.message_1.id,))
        data = {
            'text': 'test text'
        }
        json_data = json.dumps(data)

        self.client.force_login(self.user2)
        response = self.client.delete(url, data=json_data, content_type='application/json')

        self.assertEquals(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEquals(3, Message.objects.all().count())
