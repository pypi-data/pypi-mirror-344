from djx_websocket.models import UserSocket
from rest_framework import serializers


class UserSocketSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSocket
        fields = ("id", "key", "category", "user",)
