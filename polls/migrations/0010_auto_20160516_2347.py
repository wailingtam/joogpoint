# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-16 21:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_auto_20160516_2258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='establishment',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='establishment_plays', to='establishments.Establishment'),
        ),
    ]