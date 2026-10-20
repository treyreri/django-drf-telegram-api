from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from groups.models import Group, GroupMember
from .models import GroupMessage
from .serializers import GroupMessageSerializer
class GroupMessageListCreateView(generics.ListCreateAPIView):
    serializer_class = GroupMessageSerializer
    def get_group(self):
        group = get_object_or_404(Group, pk=self.kwargs["group_id"])
        if not GroupMember.objects.filter(group=group, user=self.request.user).exists(): raise PermissionDenied("Group members only.")
        return group
    def get_queryset(self): return GroupMessage.objects.filter(group=self.get_group()).select_related("sender", "group")
    def perform_create(self, serializer): serializer.save(group=self.get_group(), sender=self.request.user)
class GroupMessageDeleteView(generics.DestroyAPIView):
    serializer_class = GroupMessageSerializer
    def get_queryset(self): return GroupMessage.objects.filter(sender=self.request.user)
