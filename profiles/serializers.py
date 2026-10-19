from rest_framework import serializers
from .models import Profile, Avatar
from accounts.models import Account

class ProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", required=False)
    first_name = serializers.CharField(source="user.first_name", required=False, allow_blank=True)
    last_name = serializers.CharField(source="user.last_name", required=False, allow_blank=True)
    phone_number = serializers.CharField(source="user.phone_number", read_only=True)
    class Meta:
        model = Profile
        fields = ("id", "user_id", "phone_number", "username", "first_name", "last_name", "bio", "city", "birth_date", "created_at")
        read_only_fields = ("id", "user_id", "phone_number", "created_at")
    def validate_username(self, value):
        user = self.context["request"].user
        if Account.objects.filter(username=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value
    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        for key, value in user_data.items(): setattr(instance.user, key, value)
        if user_data: instance.user.save()
        return super().update(instance, validated_data)

class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = ("id", "image", "created_at")
        read_only_fields = ("id", "created_at")
    def validate_image(self, value):
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("Image must be 5 MB or smaller.")
        if value.content_type not in ("image/jpeg", "image/png", "image/webp"):
            raise serializers.ValidationError("Only JPEG, PNG, and WEBP images are allowed.")
        return value
