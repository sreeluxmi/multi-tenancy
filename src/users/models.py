from django.contrib.auth.models import AbstractUser
from django.db import models
from tenantapp.models import Client


class User(AbstractUser):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
