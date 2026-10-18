from rest_framework import serializers
from accounts.models import Account
from .models import Group, GroupMember
class GroupSerializer(serializers.ModelSerializer):
    owner = serializers.IntegerField(read_only=True)
    class Meta:
        model = Group
        fields = ("id", "title", "owner", "avatar", "created_at")
        read_only_fields = ("id", "owner", "created_at")
class GroupMemberSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    class Meta:
        model = GroupMember
        fields = ("id", "group", "user", "role", "joined_at")
        read_only_fields = ("id", "group", "joined_at")
