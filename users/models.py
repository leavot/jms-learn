from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=32)
    wechat = models.CharField(max_length=128)

    def __str__(self):
        return "%s <%s>" % (self.username, self.name)
