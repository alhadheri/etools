# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-07-31 10:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('action_points', '0007_auto_20180731_0920'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actionpoint',
            name='category'
        ),
        migrations.RenameField(
            model_name='actionpoint',
            old_name='category1',
            new_name='category'
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
