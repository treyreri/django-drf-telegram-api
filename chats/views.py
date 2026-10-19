from django.db.models import Q
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Chat
from .serializers import ChatSerializer
from .permissions import IsChatParticipant

class ChatListCreateView(generics.ListCreateAPIView):
    serializer_class = ChatSerializer
    def get_queryset(self): return Chat.objects.filter(Q(user_1=self.request.user) | Q(user_2=self.request.user)).select_related("user_1", "user_2")
    @transaction.atomic
    def perform_create(self, serializer):
        other = serializer.validated_data["user_2"]
        a, b = sorted([self.request.user, other], key=lambda u: u.pk)
        existing = Chat.objects.filter(user_1=a, user_2=b).first()
        if existing:
            raise ValidationError({"detail": f"Chat already exists (id={existing.pk})."})
        serializer.save(user_1=a, user_2=b)

class ChatDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated, IsChatParticipant]
    def get_queryset(self): return Chat.objects.filter(Q(user_1=self.request.user) | Q(user_2=self.request.user)).select_related("user_1", "user_2")
