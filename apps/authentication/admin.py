# Register your models here.
from django.contrib import admin

from apps.authentication.models import (
    OTPCode,
    AuditLog,
    LoginAttempt
)


admin.site.register(OTPCode)

admin.site.register(LoginAttempt)

admin.site.register(AuditLog)