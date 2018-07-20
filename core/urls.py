from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from core.schema import SwaggerSchemaView

urlpatterns = [
    url(r'^api/$', SwaggerSchemaView.as_view(), name='docs'),
    url(r'^api/', include('core.api')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^', include('shorteners.urls')),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
