from django.contrib.auth import get_user_model
from django.db import models

from .functions import default_uuid4

UserModel = get_user_model()


class Socket(models.Model):
    name = models.CharField(max_length=255, default=default_uuid4)
    category = models.CharField(max_length=20, default="user")

    class Meta:
        abstract = True

    def key(self):
        return f"U-{self.pk}-{self.name}"


class UserSocket(Socket):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
