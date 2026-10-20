from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Group, GroupMember
from .serializers import GroupSerializer, GroupMemberSerializer

class GroupListCreateView(generics.ListCreateAPIView):
    serializer_class = GroupSerializer
    def get_queryset(self): return Group.objects.filter(members__user=self.request.user).distinct().select_related("owner")
    @transaction.atomic
    def perform_create(self, serializer):
        group = serializer.save(owner=self.request.user)
        GroupMember.objects.create(group=group, user=self.request.user, role="owner")

class GroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GroupSerializer
    http_method_names = ["get", "patch", "delete", "head", "options"]
    def get_queryset(self): return Group.objects.filter(members__user=self.request.user).distinct()
    def perform_update(self, serializer):
        membership = get_object_or_404(GroupMember, group=self.get_object(), user=self.request.user)
        if membership.role not in ("owner", "admin"): raise PermissionDenied("Only group owners and admins can edit the group.")
        serializer.save(owner=self.get_object().owner)
    def perform_destroy(self, instance):
        if instance.owner_id != self.request.user.pk: raise PermissionDenied("Only the owner can delete the group.")
        instance.delete()

class GroupMemberListCreateView(generics.ListCreateAPIView):
    serializer_class = GroupMemberSerializer
    def get_group(self): return get_object_or_404(Group, pk=self.kwargs["group_id"])
    def get_queryset(self):
        group = self.get_group()
        if not GroupMember.objects.filter(group=group, user=self.request.user).exists(): raise PermissionDenied("Group members only.")
        return GroupMember.objects.filter(group=group).select_related("user")
    def perform_create(self, serializer):
        group = self.get_group()
        actor = get_object_or_404(GroupMember, group=group, user=self.request.user)
        if actor.role not in ("owner", "admin"): raise PermissionDenied("Only owners and admins can add members.")
        target = serializer.validated_data["user"]
        if GroupMember.objects.filter(group=group, user=target).exists(): raise ValidationError({"user":"User is already a member."})
        serializer.save(group=group, role="member")

class GroupMemberRoleView(generics.UpdateAPIView):
    serializer_class = GroupMemberSerializer
    http_method_names = ["patch", "head", "options"]
    def get_queryset(self):
        group = get_object_or_404(Group, pk=self.kwargs["group_id"])
        if group.owner_id != self.request.user.pk: raise PermissionDenied("Only the group owner can change roles.")
        return GroupMember.objects.filter(group=group)
    def perform_update(self, serializer):
        role = serializer.validated_data.get("role", serializer.instance.role)
        if role not in ("admin", "member"): raise ValidationError({"role":"Use admin or member; ownership transfer is separate."})
        serializer.save()

class LeaveGroupView(APIView):
    def delete(self, request, group_id):
        membership = get_object_or_404(GroupMember, group_id=group_id, user=request.user)
        if membership.role == "owner": return Response({"detail":"The owner cannot leave without transferring ownership."}, status=status.HTTP_400_BAD_REQUEST)
        membership.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
