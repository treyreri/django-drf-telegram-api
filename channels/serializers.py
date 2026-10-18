from rest_framework import serializers
from .models import Channel, Following
class ChannelSerializer(serializers.ModelSerializer):
    owner = serializers.IntegerField(read_only=True)
    class Meta:
        model = Channel
        fields = ("id", "title", "description", "type", "owner", "slug", "created_at")
        read_only_fields = ("id", "owner", "slug", "created_at")
class FollowingSerializer(serializers.ModelSerializer):
    channel_title = serializers.CharField(source="channel.title", read_only=True)
    channel_slug = serializers.CharField(source="channel.slug", read_only=True)
    class Meta:
        model = Following
        fields = ("id", "channel", "channel_title", "channel_slug", "created_at")
        read_only_fields = fields
