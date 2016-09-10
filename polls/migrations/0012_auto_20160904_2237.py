# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-09-04 20:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0011_playlist_explicit_lyrics'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='artist',
            field=models.CharField(default='Unknown artist', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='track',
            name='title',
            field=models.CharField(default='Unknown title', max_length=100),
            preserve_default=False,
        ),
    ]
