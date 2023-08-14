from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from message.views import MessageViews, MessageDeleteView, MessageUpdateView, vuejs_page

urlpatterns = [
    path('', MessageViews.as_view(), name='home'),
    path('<int:id>/delete/', MessageDeleteView.as_view(), name='message_delete'),
    path('<int:id>/edit/', MessageUpdateView.as_view(), name='message_update'),

    path('vuejs/', vuejs_page, name='vuejs'),

]
