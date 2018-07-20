from allauth.account.models import EmailConfirmationHMAC, EmailConfirmation
from allauth.account import app_settings as allauth_settings
from allauth.account.utils import complete_signup as complete_signup_signal
from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import (
    AuthTokenSerializer,
    CreateUserSerializer,
    UserCreatedSerializer,
    VerifyEmailSerializer,
    RecoveryPasswordSerializer,
    RecoveryPasswordConfirmSerializer,
)
from .permissions import AnonymousUserOnlyPermission


User = get_user_model()


class ObtainAuthToken(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class UserRegisterEndpoint(generics.CreateAPIView):
    """
    Endpoint to register users
    """

    permission_classes = (AnonymousUserOnlyPermission,)
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(**serializer.data)
            complete_signup_signal(
                request=self.request,
                user=user,
                email_verification=allauth_settings.EMAIL_VERIFICATION,
                success_url=None
            )
            return Response(
                {"detail": "Verification e-mail sent."},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailEndpoint(generics.GenericAPIView):
    """
    Endpoint verify user email
    """
    permission_classes = (AnonymousUserOnlyPermission,)
    serializer_class = VerifyEmailSerializer

    def get_email_confirmation(self, verification_key=None):
        """
        Retreive EmailConfirmation object for provided `key`
        Throws 404 if does not exist
        """
        email_confirmation = EmailConfirmationHMAC.from_key(verification_key)
        if not email_confirmation:
            try:
                email_confirmation = EmailConfirmation.objects.all_valid(
                ).select_related("email_address__user").get(key=verification_key.lower())
            except EmailConfirmation.DoesNotExist:
                raise Http404()
        return email_confirmation

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        verification_key = serializer.validated_data['key']
        confirmation = self.get_email_confirmation(verification_key)
        confirmation.confirm(self.request)
        user = confirmation.email_address.user
        return Response(UserCreatedSerializer(instance=user).data)


class RecoveryPasswordEndpoint(generics.GenericAPIView):
    """
    Endpoint recovery password send e-mail
    """
    permission_classes = (AnonymousUserOnlyPermission,)
    serializer_class = RecoveryPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Recovery password e-mail has been sent."}
        )


class PasswordRecoveryConfirmEndpoint(generics.GenericAPIView):
    """
    Password recovery e-mail link is confirm
    """
    serializer_class = RecoveryPasswordConfirmSerializer
    permission_classes = (AnonymousUserOnlyPermission,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Your password has been changed successfully"}
        )
