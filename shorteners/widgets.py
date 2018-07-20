from django import forms
from django.utils.crypto import get_random_string
from django.forms.utils import flatatt
from django.utils.safestring import mark_safe


class GenerateRandomStringWidget(forms.TextInput):
    """
    Custom widget to generate random string
    """
    def render(self, name, value, attrs=None):
        super().render(name, value, attrs)
        attrs['id'] = attrs['id'].replace('-', '_')  # needed for inlines
        flat_attrs = flatatt(attrs)
        html = '''
<input %(attrs)s name="%(name)s" type="input" value="%(value)s"/>
<span id="__action__%(id)s__show_button">
<a href="javascript:generate_string_%(id)s()">Generate</a></span>
<script type="text/javascript">
function randomString(len) {
    charSet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var randomString = '';
    for (var i = 0; i < len; i++) {
        var randomPoz = Math.floor(Math.random() * charSet.length);
        randomString += charSet.substring(randomPoz,randomPoz+1);
    }
    return randomString;
}
function generate_string_%(id)s() {
    document.getElementById("%(id)s").setAttribute('value', randomString(12));
}
</script>
        ''' % {
            'attrs': flat_attrs,
            'name': name,
            'id': attrs['id'],
            'value': value if value else get_random_string(length=12),
        }
        return mark_safe(html)
