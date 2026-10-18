from rest_framework import serializers
from .models import GroupMessage
class GroupMessageSerializer(serializers.ModelSerializer):
    sender = serializers.IntegerField(read_only=True)
    class Meta:
        model = GroupMessage
        fields = ("id", "group", "sender", "content", "created_at")
        read_only_fields = ("id", "group", "sender", "created_at")
    def validate_content(self, value):
        if not value.strip(): raise serializers.ValidationError("Message cannot be empty.")
        return value
