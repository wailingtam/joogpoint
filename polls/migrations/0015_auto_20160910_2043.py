# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-09-10 18:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0014_track_in_playlist'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='track',
            unique_together=set([]),
        ),
    ]
