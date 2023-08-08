from django.contrib.auth import get_user_model
from django.test import TestCase

from message.models import Message
from api.serializers import MessageSerializer

User = get_user_model()

class MessageSerializerTestCase(TestCase):
    def test_ok(self):
        self.user = User.objects.create(username='test_username')

        message_1 = Message.objects.create(text='test text 1', author=self.user)
        message_2 = Message.objects.create(text='test text 2', author=self.user)

        data = MessageSerializer([message_1, message_2], many=True).data
        expected_data = [
            {
                'id': message_1.id,
                'text': 'test text 1',
                'author': self.user.id
            },
            {
                'id': message_2.id,
                'text': 'test text 2',
                'author': self.user.id
            },
        ]

        self.assertEquals(expected_data, data)
