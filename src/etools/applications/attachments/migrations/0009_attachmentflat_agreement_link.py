# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-07-20 17:23
from __future__ import unicode_literals

from django.urls import reverse
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attachments', '0008_auto_20180717_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachmentflat',
            name='object_link',
            field=models.URLField(blank=True, verbose_name='Object Link'),
        ),
    ]
