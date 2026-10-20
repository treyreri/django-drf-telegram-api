from django.shortcuts import render

from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from channels.models import Channel, Following
from .models import Post
from .serializers import PostSerializer

class ChannelPostListCreateView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    def get_channel(self):
        channel = get_object_or_404(Channel, pk=self.kwargs["channel_id"])
        if channel.type == "private" and channel.owner_id != self.request.user.pk and not Following.objects.filter(channel=channel, user=self.request.user).exists():
            raise PermissionDenied("Private channel access denied.")
        return channel
    def get_queryset(self): return Post.objects.filter(channel=self.get_channel()).select_related("channel")
    def perform_create(self, serializer):
        channel = self.get_channel()
        if channel.owner_id != self.request.user.pk: raise PermissionDenied("Only the channel owner can publish posts.")
        serializer.save(channel=channel)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    def get_queryset(self):
        from django.db.models import Q
        return Post.objects.filter(Q(channel__type="public") | Q(channel__owner=self.request.user) | Q(channel__followers__user=self.request.user)).distinct().select_related("channel")
    def _check_owner(self, obj):
        if obj.channel.owner_id != self.request.user.pk: raise PermissionDenied("only the channel owner can change posts")
    def perform_update(self, serializer): self._check_owner(serializer.instance); serializer.save(channel=serializer.instance.channel)
    def perform_destroy(self, instance): self._check_owner(instance); instance.delete()
