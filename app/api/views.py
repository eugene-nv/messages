
from rest_framework.viewsets import ModelViewSet
from message.models import Message
from .permissions import IsAuthorOrReadOnly
from .serializers import MessageSerializer


class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthorOrReadOnly, ]

    def perform_create(self, serializer):
        serializer.validated_data['author'] = self.request.user
        serializer.save()
