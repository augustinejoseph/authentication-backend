from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from user_management.models import User


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserCreateSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        print(attrs)
        password = make_password(attrs.get("password"))
        attrs["password"] = password
        return attrs

    class Meta:
        model = User
        fields = "__all__"


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "phone_number",
            "is_delete",
            "is_verified",
            "last_device",
        ]
