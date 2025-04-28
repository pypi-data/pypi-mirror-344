from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from djx_websocket.models import UserSocket
from djx_websocket.serializers.user_socket_serializers import UserSocketSerializer


class UserSocketViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = UserSocketSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = UserSocket.objects.filter(user_id=self.request.user.id)
        return queryset

    def get_serializer_class(self):
        return super().get_serializer_class()

    def get_object(self):
        instance, _ = UserSocket.objects.get_or_create(user=self.request.user)
        return instance
