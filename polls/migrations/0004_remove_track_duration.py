# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-08 20:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_track_duration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='track',
            name='duration',
        ),
    ]