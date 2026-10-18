from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Account

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, trim_whitespace=False)
    class Meta:
        model = Account
        fields = ("id", "phone_number", "password", "username", "first_name", "last_name")
        read_only_fields = ("id",)
    def validate_phone_number(self, value):
        value = value.strip()
        if len(value) < 7 or len(value) > 20:
            raise serializers.ValidationError("Enter a valid phone number.")
        return value
    def validate_password(self, value):
        try:
            password_validation.validate_password(value)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(list(exc.messages))
        return value
    def create(self, validated_data):
        password = validated_data.pop("password")
        return Account.objects.create_user(password=password, **validated_data)

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("id", "phone_number", "username", "first_name", "last_name", "date_joined")
        read_only_fields = fields

class PhoneTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = Account.USERNAME_FIELD

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, trim_whitespace=False)
    new_password = serializers.CharField(write_only=True, trim_whitespace=False)
    def validate_new_password(self, value):
        try:
            password_validation.validate_password(value, self.context["request"].user)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(list(exc.messages))
        return value
    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value
