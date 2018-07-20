Start new project like this
`django-admin.py startproject --template=https://github.com/khorolets/project_template/zipball/refactor_template project`

Rename `project` to YOUR real project name.

Update local settings in settings directrory.

You need to provide random string for `SECRET_KEY` in `project/core/settings/base.py`.

You can use following oneliner:

```shell
$ python -c "import string; from django.utils.crypto import get_random_string; print (\"SECRET_KEY = '%s'\" % get_random_string(length=75, allowed_chars=''.join(set(string.digits + string.ascii_letters + string.punctuation) - set('\'\"'))))"
```

or just generate it online (if You are using python 3) with  [django-secret-key-generator](http://www.miniwebtool.com/django-secret-key-generator/)

Then just copy-paste it to `project/core/settings/base.py`

Then

```shell
$ python manage migrate
$ python manage createsuperuser
$ python manage runserver
```

You're ready to go!
