# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-08 20:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('establishments', '0004_auto_20160409_2116'),
    ]

    operations = [
        migrations.AddField(
            model_name='establishment',
            name='lastfm_username',
            field=models.CharField(default='wailingtam', max_length=100),
            preserve_default=False,
        ),
    ]
