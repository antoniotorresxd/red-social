from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .manager import AccountManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    birthdate = models.DateField()
    id_student = models.CharField(max_length=10, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'birthdate']

    objects = AccountManager()

    def __str__(self):
        return self.name
