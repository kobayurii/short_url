from django import forms
from shorteners import widgets
from .models import ShortURL


class ShortURLCreateForm(forms.ModelForm):
    """
    Form to create short url
    """
    short = forms.CharField(widget=widgets.GenerateRandomStringWidget())

    class Meta:
        model = ShortURL
        fields = ('url', 'short')


class ShortURLEditForm(forms.ModelForm):
    """
    Form to edit short url
    """
    short = forms.CharField(widget=widgets.GenerateRandomStringWidget())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['created_at'].widget.attrs['readonly'] = True
            self.fields['clicks'].widget.attrs['readonly'] = True

    class Meta:
        model = ShortURL
        fields = ('url', 'short', 'text', 'created_at', 'clicks')

    def clean(self):
        """
        Modify the text in the following way:
        after each word of six characters there should be an icon “TM”
        """
        data = super().clean()
        data['text'] = ' '.join(
            [word + '™' if len(word) == 6 else word for word in data['text'].split(' ')]
        )
        return data
