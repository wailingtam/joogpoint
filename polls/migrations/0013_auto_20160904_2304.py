# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-09-04 21:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0012_auto_20160904_2237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='voters',
            field=models.ManyToManyField(blank=True, related_name='voted', to=settings.AUTH_USER_MODEL),
        ),
    ]
