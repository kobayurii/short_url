import os
import random
import re
import string

from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model


User = get_user_model()


def create_password(length=13, strong=False):
    """
    Generates strong password of specified length
    :param length: length of password, default 13
    :return: string of password
    """

    chars = string.ascii_letters + string.digits
    chars += '!@#$%^&*()_' if strong else ''
    random.seed = (os.urandom(1024))
    return ''.join(random.choice(chars) for i in range(length))


def mail(email, subject, html_email):
    try:
        send_mail(
            subject,
            html_email,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=True,
            html_message=html_email
        )
        return True
    except:
        return False


def validate_username(username):
    """
    Helper to validate if username is valid and hasn't been taken already
    :param username: string
    :return: boolean
    """
    user_with_the_same_username = User.objects.filter(username=username).count()
    if user_with_the_same_username:
        return False

    match_valid_pattern = re.findall(r'([\w\d\-\.]{3,50})', username)
    if match_valid_pattern:
        return len(username) == len(match_valid_pattern[0])

    return False
