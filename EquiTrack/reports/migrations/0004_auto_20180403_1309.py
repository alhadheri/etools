# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-04-03 13:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0003_make_not_nullable'),
    ]

    operations = [
        migrations.AddField(
            model_name='appliedindicator',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='appliedindicator',
            name='is_high_frequency',
            field=models.BooleanField(default=False),
        ),
    ]