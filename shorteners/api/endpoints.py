from django.utils.crypto import get_random_string
from rest_framework import generics, status
from rest_framework.response import Response
from shorteners.models import ShortURL
from .serializers import ShortURLSerializer, CreateShortURLSerializer


class ShortUrlMixin(object):
    """
    Short url endpoints mixin
    """
    queryset = ShortURL.objects.all().order_by('-created_at')
    serializer_class = CreateShortURLSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        self.serializer_class = ShortURLSerializer
        return super().get(request, *args, **kwargs)


class MyShortUrlsEndpoint(ShortUrlMixin, generics.ListCreateAPIView):
    """
    Endpoint to create short url or get all users short urls
    """
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            data['user'] = request.user
            if not data.get('short', None):
                data['short'] = get_random_string(length=12)
            obj = ShortURL.objects.create(**data)
            return Response(ShortURLSerializer(instance=obj).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShortUrlEndpoint(ShortUrlMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Endpoint to get or update or delete short url by id
    """
    lookup_url_kwarg = 'pk'
    lookup_field = 'pk'
