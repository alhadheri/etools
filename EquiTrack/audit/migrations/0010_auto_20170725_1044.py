# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-07-25 10:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('audit', '0009_merge'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='financialfinding',
            unique_together=set([]),
        ),
        migrations.AlterUniqueTogether(
            name='finding',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='financialfinding',
            name='finding_number',
        ),
        migrations.RemoveField(
            model_name='finding',
            name='finding_number',
        ),
    ]
