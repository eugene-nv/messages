from rest_framework.serializers import ModelSerializer
from message.models import Message


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'