from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views import generic
from django.conf import settings
from shorteners.models import ShortURL
from .forms import ShortURLCreateForm, ShortURLEditForm


class IndexView(generic.ListView, generic.FormView):
    """
    Index view and create shot url
    """
    form_class = ShortURLCreateForm
    template_name = 'index.html'
    queryset = ShortURL.objects.all().order_by('-created_at')
    context_object_name = 'short_urls'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['domain'] = settings.BASE_URL
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            data = form.cleaned_data
            data['user'] = request.user
            self.object = ShortURL.objects.create(**data)
            return redirect('edit', self.object.pk)
        else:
            self.object_list = self.get_queryset()
            return self.form_invalid(form)


class EditShortUrlView(generic.DetailView, generic.CreateView):
    """
    View to retrieve and edit short url
    """
    model = ShortURL
    form_class = ShortURLEditForm
    template_name = 'shortener.html'
    context_object_name = 'short_url'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            data = form.cleaned_data
            self.object.short = data['short']
            self.object.text = data['text']
            self.object.save()
            return redirect('/')
        else:
            return self.form_invalid(form)


class DeleteShortUrlView(generic.DetailView):
    """
    View to delete short url
    """
    model = ShortURL

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        self.get_object().delete()
        return redirect('/')


class RedirectView(generic.DetailView):
    """
    View redirect short url to base base url
    """
    model = ShortURL
    slug_field = 'short'
    slug_url_kwarg = 'short'

    def get(self, request, *args, **kwargs):
        short_url = self.get_object()
        short_url.clicks += 1
        short_url.save()
        return HttpResponseRedirect(short_url.url)
