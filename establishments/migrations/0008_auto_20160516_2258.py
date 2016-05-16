# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-16 20:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('establishments', '0007_establishment_check_ins'),
    ]

    operations = [
        migrations.RenameField(
            model_name='establishment',
            old_name='check_ins',
            new_name='customers',
        ),
        migrations.AlterField(
            model_name='establishment',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner_of', to=settings.AUTH_USER_MODEL),
        ),
    ]
