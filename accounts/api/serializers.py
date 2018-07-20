from allauth.account.forms import ResetPasswordForm, UserTokenForm
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import SetPasswordForm
from rest_framework import serializers, exceptions
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise exceptions.ValidationError(msg)
            else:
                msg = _('Unable to log in with provided credentials.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)

        data['user'] = user
        return data


class CreateUserSerializer(serializers.ModelSerializer):
    """
    Serializer to create new user
    """
    password = serializers.CharField(required=True)
    username = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'password',
        )


class UserCreatedSerializer(CreateUserSerializer):
    """
    Serializer to represent new user
    """
    token = serializers.SerializerMethodField(read_only=True)

    class Meta(CreateUserSerializer.Meta):
        fields = CreateUserSerializer.Meta.fields + (
            'token',
        )

    def get_token(self, obj):
        if obj.auth_token:
            return obj.auth_token.key
        return None


class VerifyEmailSerializer(serializers.Serializer):
    """
    Verify user email Serializer
    """
    key = serializers.CharField()


class RecoveryPasswordSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """
    email = serializers.EmailField()

    def validate_email(self, email):
        self.form = ResetPasswordForm(data=self.initial_data)
        if not self.form.is_valid():
            raise serializers.ValidationError(self.form.errors['email'])
        return email

    def save(self):
        request = self.context.get('request')
        self.form.save(request)


class RecoveryPasswordConfirmSerializer(serializers.Serializer):
    """
    Serializer for confirming password reset and setting a new password.
    """
    key = serializers.CharField(required=True)
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)
    set_password_form = SetPasswordForm

    def validate(self, attrs):
        user = self._get_user(attrs)
        self.form = self.set_password_form(
            user=user,
            data=self.initial_data
        )
        if not self.form.is_valid():
            raise serializers.ValidationError(self.form.errors)
        return attrs

    def save(self):
        self.form.save()

    def _get_user(self, attrs):
        """
        Method extracts ``key`` from ``attrs`` and unpacks it to ``uid`` and ``token``.
        Tries to return ``User`` for provided ``uid`` and ``token``.
        Throws ``exceptions.ValidationError`` if ``User`` does not exist.
        """

        msg = "The password reset token was invalid."

        uid, _, token = attrs['key'].partition('-')
        if not len(uid) or not len(token):
            raise exceptions.ValidationError(msg)
        user_token = UserTokenForm(
            data={
                'uidb36': uid,
                'key': token
            }
        )
        if not user_token.is_valid():
            raise exceptions.ValidationError(msg)
        return user_token.reset_user
