from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Channel, Following
from .serializers import ChannelSerializer, FollowingSerializer

class ChannelListCreateView(generics.ListCreateAPIView):
    serializer_class = ChannelSerializer
    filterset_fields = ["type"]
    def get_queryset(self):
        # Public channels are discoverable; private channels are visible only to owner/subscribers.
        from django.db.models import Q
        return Channel.objects.filter(Q(type="public") | Q(owner=self.request.user) | Q(followers__user=self.request.user)).distinct().select_related("owner")
    def perform_create(self, serializer): serializer.save(owner=self.request.user)

class ChannelDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChannelSerializer
    def get_queryset(self):
        from django.db.models import Q
        return Channel.objects.filter(Q(type="public") | Q(owner=self.request.user) | Q(followers__user=self.request.user)).distinct()
    def perform_update(self, serializer):
        if serializer.instance.owner_id != self.request.user.pk: raise PermissionDenied("Only the channel owner can update it.")
        serializer.save(owner=serializer.instance.owner)
    def perform_destroy(self, instance):
        if instance.owner_id != self.request.user.pk: raise PermissionDenied("Only the channel owner can delete it.")
        instance.delete()

class FollowChannelView(APIView):
    def post(self, request, channel_id):
        channel = get_object_or_404(Channel, pk=channel_id)
        if channel.type == "private" and channel.owner_id != request.user.pk:
            raise PermissionDenied("The owner must grant access to this private channel before you can follow it.")
        if Following.objects.filter(user=request.user, channel=channel).exists():
            raise ValidationError({"detail":"Already following this channel."})
        Following.objects.create(user=request.user, channel=channel)
        return Response({"detail":"Following channel."}, status=status.HTTP_201_CREATED)
    def delete(self, request, channel_id):
        following = get_object_or_404(Following, user=request.user, channel_id=channel_id)
        following.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FollowingListView(generics.ListAPIView):
    serializer_class = FollowingSerializer
    def get_queryset(self): return Following.objects.filter(user=self.request.user).select_related("channel")

class IsFollowingView(APIView):
    def get(self, request, channel_id):
        channel = get_object_or_404(Channel, pk=channel_id)
        if channel.type == "private" and channel.owner_id != request.user.pk and not Following.objects.filter(channel=channel, user=request.user).exists():
            raise PermissionDenied("Private channel access denied.")
        return Response({"channel_id":channel.pk, "is_following":Following.objects.filter(channel=channel, user=request.user).exists()})
