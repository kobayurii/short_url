from rest_framework import serializers
from shorteners.models import ShortURL


class ShortURLSerializer(serializers.ModelSerializer):
    """
    Serializer to represent short url
    """
    class Meta:
        model = ShortURL
        fields = (
            'id',
            'short',
            'url',
            'text',
            'created_at',
            'clicks'
        )


class CreateShortURLSerializer(serializers.ModelSerializer):
    """
    Serializer to create or update short url
    """
    short = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = ShortURL
        fields = (
            'short',
            'url',
            'text',
        )

    def validate_text(self, text):
        if text:
            text = ' '.join(
                [word + '™' if len(word) == 6 else word for word in text.split(' ')]
            )
        return text

    def validate_short(self, short):
        if short:
            if ShortURL.objects.filter(short=short).count():
                raise serializers.ValidationError('This short already exists.')
        return short
