# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-19 20:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ShortURL',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short', models.CharField(max_length=64, unique=True)),
                ('url', models.URLField()),
                ('text', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('clicks', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
