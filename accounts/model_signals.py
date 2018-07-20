"""
File for different signals for accounts' models
"""
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver


User = get_user_model()


@receiver(post_save, sender=User)
def default_username(sender, instance=None, **kwargs):
    """
    Signal to set default username if none is provided
    """
    if len(instance.username.strip()) == 0:
        instance.username = 'id%d' % instance.pk
        instance.save()
