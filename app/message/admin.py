from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Message


@admin.register(Message)
class MessageAdmin(ModelAdmin):
    pass