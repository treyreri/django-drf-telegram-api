from rest_framework import serializers
from .models import Post
class PostSerializer(serializers.ModelSerializer):
    channel = serializers.IntegerField(read_only=True)
    class Meta:
        model = Post
        fields = ("id", "channel", "title", "description", "content", "created_at", "updated_at")
        read_only_fields = ("id", "channel", "created_at", "updated_at")
        