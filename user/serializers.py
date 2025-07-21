from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from user.utils import generate_token
from .models import User
from django.contrib.auth import authenticate


class SignUpSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone_number = serializers.CharField()
    password = serializers.CharField()
    confirm_password = serializers.CharField(required=True)

    def validate_phone_number(self, value):
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("This phone number is already exists!")
        return value

    def validate(self, data):
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        if password != confirm_password:
            raise serializers.ValidationError("Passwords are not the same!")
        if password:
            validate_password(password)
            validate_password(confirm_password)

        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()

    def auth_validate(self, data):
        phone_number = data.get("phone_number")
        password = data.get("password")

        user = authenticate(phone_number=phone_number, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid Credentails")

        self.user = user

    def validate(self, data):
        self.auth_validate(data)
        token = generate_token(self.user)
        data["token"] = token
        return data
