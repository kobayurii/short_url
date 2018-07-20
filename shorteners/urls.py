from django.conf.urls import url
from shorteners import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(
        r'^$',
        login_required(views.IndexView.as_view()),
        name='shortener'
    ),
    url(
        r'^(?P<pk>[0-9]+)/$',
        login_required(views.EditShortUrlView.as_view()),
        name='edit'
    ),
    url(
        r'^(?P<pk>[0-9]+)/delete/$',
        login_required(views.DeleteShortUrlView.as_view()),
        name='delete'
    ),
    url(
        r'^(?P<short>[\w\d\-\.\_]{1,64})/$',
        views.RedirectView.as_view(),
        name='short'
    ),
]
