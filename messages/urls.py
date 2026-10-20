
from django.urls import path
from .views import ChatMessageListCreateView, MessageDeleteView

urlpatterns = [
    path("chats/<int:chat_id>/", ChatMessageListCreateView.as_view(), name="chat-messages"),
    path("<int:pk>/", MessageDeleteView.as_view(), name="message-delete"),
]
