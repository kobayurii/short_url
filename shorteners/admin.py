from django.contrib import admin
from shorteners.models import ShortURL


@admin.register(ShortURL)
class ShortURLAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'url',
        'short',
        'text',
        'created_at',
        'clicks',
    )
