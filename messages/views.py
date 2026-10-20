from django.shortcuts import render

from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from chats.models import Chat
from .models import Message
from .serializers import MessageSerializer

class ChatMessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    def get_chat(self):
        chat = get_object_or_404(Chat, pk=self.kwargs["chat_id"])
        if self.request.user.pk not in (chat.user_1_id, chat.user_2_id): raise PermissionDenied("You are not a participant in this chat.")
        return chat
    def get_queryset(self): return Message.objects.filter(chat=self.get_chat()).select_related("sender", "chat")
    def perform_create(self, serializer): serializer.save(chat=self.get_chat(), sender=self.request.user)

class MessageDeleteView(generics.DestroyAPIView):
    serializer_class = MessageSerializer
    def get_queryset(self): return Message.objects.filter(sender=self.request.user)
