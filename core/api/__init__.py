from django.conf.urls import url, include

urlpatterns = [
    url(r'^v1/', include('core.api.v1', namespace='v1')),
]
