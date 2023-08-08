from django.forms import ModelForm, HiddenInput

from .models import Message


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = '__all__'
        widgets = {'author': HiddenInput()}