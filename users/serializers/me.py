from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username"
        )

    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
