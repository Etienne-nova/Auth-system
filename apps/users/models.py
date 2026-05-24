from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import UserManager


class Permission(models.Model):

    name = models.CharField(
        max_length=255,
        unique=True
    )

    code = models.CharField(
        max_length=255,
        unique=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):

        return self.name

class Role(models.Model):

    name = models.CharField(
        max_length=255,
        unique=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    permissions = models.ManyToManyField(
        Permission,
        blank=True
    )

    def __str__(self):

        return self.name

class User(AbstractUser):
    objects = UserManager()

    email = models.EmailField(unique=True)

    is_email_verified = models.BooleanField(default=False)

    is_mfa_enabled = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)
    
    roles = models.ManyToManyField(Role, blank=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email