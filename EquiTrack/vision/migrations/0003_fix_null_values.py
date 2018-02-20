# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2018-02-19 16:18
from __future__ import unicode_literals

from django.db import migrations, models

from utils.common.migrating import fix_null_values


def fix_nulls(apps, schema):
    # Change null values in these fields to empty strings
    fix_null_values(
        apps.get_model('vision.visionsynclog'),
        [
            'details',
            'exception_message',
        ]
    )

class Migration(migrations.Migration):

    dependencies = [
        ('vision', '0002_visionsynclog_details'),
    ]

    operations = [
        migrations.RunPython(fix_nulls, migrations.RunPython.noop)
    ]
