from django.db import models

# Create your models here.
from django.conf import settings

from django.utils import timezone

from datetime import timedelta

import secrets

import hashlib

class OTPCode(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    code = models.CharField(max_length=6)

    created_at = models.DateTimeField(auto_now_add=True)

    expires_at = models.DateTimeField()

    is_used = models.BooleanField(default=False)

    def is_expired(self):

        return timezone.now() > self.expires_at

    @staticmethod
    def default_expiry():

        return timezone.now() + timedelta(minutes=5)

    def save(self, *args, **kwargs):

        if not self.expires_at:
            self.expires_at = self.default_expiry()

        super().save(*args, **kwargs)

    def __str__(self):

        return f"{self.user.email} - {self.code}"



class AuditLog(models.Model):

    EVENT_CHOICES = [

        ('login_success', 'Login Success'),

        ('login_failed', 'Login Failed'),

        ('logout', 'Logout'),

        ('mfa_verified', 'MFA Verified'),

        ('email_verified', 'Email Verified'),

        ('sso_login', 'SSO Login'),
    ]

    user = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.SET_NULL,

        null=True,

        blank=True
    )

    event_type = models.CharField(

        max_length=100,

        choices=EVENT_CHOICES
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    user_agent = models.TextField(
        null=True,
        blank=True
    )

    metadata = models.JSONField(
        default=dict,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (
            f"{self.event_type} - "
            f"{self.created_at}"
        )    
        

class LoginAttempt(models.Model):

    email = models.EmailField()

    ip_address = models.GenericIPAddressField()

    attempts = models.IntegerField(default=0)

    is_blocked = models.BooleanField(default=False)

    blocked_until = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return f"{self.email} - {self.ip_address}"
    
class UserDevice(models.Model):

    user = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

        related_name='devices'
    )

    device_name = models.CharField(
        max_length=255
    )

    device_type = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    browser = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    ip_address = models.GenericIPAddressField()

    user_agent = models.TextField()

    last_login = models.DateTimeField(
        auto_now=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (
            f"{self.user.email} - "
            f"{self.device_name}"
        )

class UserSession(models.Model):

    user = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

        related_name='sessions'
    )

    device = models.ForeignKey(

        UserDevice,

        on_delete=models.CASCADE,

        related_name='sessions'
    )

    refresh_token = models.TextField()

    ip_address = models.GenericIPAddressField()

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    expires_at = models.DateTimeField()

    def __str__(self):

        return (
            f"{self.user.email} - "
            f"{self.ip_address}"
        )


class APIKey(models.Model):

    name = models.CharField(
        max_length=255
    )

    key_prefix = models.CharField(
        max_length=20
    )

    hashed_key = models.CharField(
        max_length=255
    )

    user = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

        related_name='api_keys'
    )

    is_active = models.BooleanField(
        default=True
    )

    expires_at = models.DateTimeField(
        null=True,
        blank=True
    )

    last_used_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (
            f"{self.name} - "
            f"{self.user.email}"
        )