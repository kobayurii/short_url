from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class ShortURL(models.Model):
    """
    Model to store short url
    """
    short = models.CharField(max_length=64, unique=True)
    url = models.URLField()
    user = models.ForeignKey(User)
    text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    clicks = models.IntegerField(default=0)
