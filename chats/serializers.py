from rest_framework import serializers
from accounts.models import Account
from .models import Chat
class ChatSerializer(serializers.ModelSerializer):
    user_2 = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    user_1 = serializers.IntegerField(read_only=True)
    class Meta:
        model = Chat
        fields = ("id", "user_1", "user_2", "created_at")
        read_only_fields = ("id", "user_1", "created_at")
    def validate_user_2(self, value):
        if value.pk == self.context["request"].user.pk:
            raise serializers.ValidationError("You cannot create a chat with yourself.")
        return value
