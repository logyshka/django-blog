from typing import Any

from django.contrib.auth import get_user_model, authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

User = get_user_model()


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "password",
        )

    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(style={"input_type": "password"}, write_only=True, required=True)

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        username = attrs.get("username").lower()
        password = attrs.get("password")
        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("Неверный логин или пароль")

        self.instance = user

        return attrs
