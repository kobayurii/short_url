from .base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'short_url_db',
        'USER': 'short',
        'PASSWORD': 'XN3T35quUGrg',
        'HOST': 'db',
        'PORT': 5432
    }
}


# CREATE DATABASE short_url_db;
# CREATE USER short with password 'XN3T35quUGrg';
# GRANT ALL PRIVILEGES ON DATABASE short_url_db to short;
