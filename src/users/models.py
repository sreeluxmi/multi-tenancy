from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class UserPermissions(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'permissions_userpermissions'
