from django.conf.urls import url, include

urlpatterns = [
    url(r'^users/', include('accounts.api.urls')),
    url(r'^shorturl/', include('shorteners.api.urls')),
]
