# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-16 21:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20160516_2347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='fav_artists',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='fav_genres',
            field=models.TextField(blank=True, null=True),
        ),
    ]
