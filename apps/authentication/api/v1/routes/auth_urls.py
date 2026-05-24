from django.urls import path

from apps.authentication.api.v1.views.login_views import LoginView
from apps.authentication.api.v1.views.register_view import (
    RegisterView
)
from apps.authentication.api.v1.views.verify_otp_view import (
    VerifyOTPView
)
from apps.authentication.api.v1.views.verify_email_view import (
    VerifyEmailView
)
from apps.authentication.api.v1.views.sso_login_view import (
    SSOLoginView
)
from apps.authentication.api.v1.views.logout_view import (
    LogoutView
)
from rest_framework_simplejwt.views import (
    TokenRefreshView
)
from apps.authentication.api.v1.views.admin_test_view import (
    AdminTestView
)
from apps.authentication.api.v1.views.forgot_password_view import (
    ForgotPasswordView
)

from apps.authentication.api.v1.views.reset_password_view import (
    ResetPasswordView
)
from apps.authentication.api.v1.views.device_list_view import (
    DeviceListView
)
from apps.authentication.api.v1.views.revoke_device_view import (
    RevokeDeviceView
)
from apps.authentication.api.v1.views.create_api_key_view import (
    CreateAPIKeyView
)
urlpatterns = [

    path(
        'login/',
        LoginView.as_view(),
        name='login'
    ),
    
    path(
        'register/',
        RegisterView.as_view(),
        name='register'
    ),
    
    path(
        'verify-otp/',
        VerifyOTPView.as_view(),
        name='verify-otp'
    ),
    
    path(
        'verify-email/',
        VerifyEmailView.as_view(),
        name='verify-email'
    ),
    path(
        'sso/login/',
        SSOLoginView.as_view(),
        name='sso-login'
    ),
    
    path(
        'logout/',
        LogoutView.as_view(),
        name='logout'
    ),
    
    path(
        'token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    
    path(
        'admin-test/',
        AdminTestView.as_view(),
        name='admin-test'
    ),
    
    path(
        'forgot-password/',
        ForgotPasswordView.as_view(),
        name='forgot-password'
    ),

    path(
        'reset-password/',
        ResetPasswordView.as_view(),
        name='reset-password'
    ),
    
    path(
        'devices/',
        DeviceListView.as_view(),
        name='devices'
    ),
    path(
        'sessions/<int:session_id>/revoke/',
        RevokeDeviceView.as_view(),
        name='revoke-device'
    ),
    path(
        'api-keys/create/',
        CreateAPIKeyView.as_view(),
        name='create-api-key'
    )
]
