from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Message(models.Model):
    text = models.TextField(verbose_name='')
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return f'ID {self.id}: {self.author} {self.text}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['id']
