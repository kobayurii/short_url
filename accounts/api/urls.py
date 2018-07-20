from django.conf.urls import url
from . import endpoints, token

urlpatterns = [
    url(
        r'^register/$',
        endpoints.UserRegisterEndpoint.as_view(),
        name='user_register'
    ),
    url(
        r'^register/verify_email/$',
        endpoints.VerifyEmailEndpoint.as_view(),
        name='user_verify_email'
    ),
    url(
        r'^password/recovery/$',
        endpoints.RecoveryPasswordEndpoint.as_view(),
        name='recovery_password'
    ),
    url(
        r'^password/recovery/confirm/$',
        endpoints.PasswordRecoveryConfirmEndpoint.as_view(),
        name='recovery_password_confirm'
    ),
    url(
        r'^token/$',
        endpoints.ObtainAuthToken.as_view(),
        name='obtain_token'
    ),
]