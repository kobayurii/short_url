from django.conf.urls import url
from shorteners.api import endpoints

urlpatterns = [
    url(
        r'^$',
        endpoints.MyShortUrlsEndpoint.as_view(),
        name='short_url'
    ),
    url(
        r'^(?P<pk>[0-9]+)/$',
        endpoints.ShortUrlEndpoint.as_view(),
        name='crud_short_url'
    ),
]
