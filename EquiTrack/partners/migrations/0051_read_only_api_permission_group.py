# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-09-20 15:23
from __future__ import unicode_literals

from django.db import migrations


def remove_permission_group(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    try:
        api_grp = Group.objects.get(name='Read-Only API')
    except Group.DoesNotExist:
        return
    api_grp.delete()

def add_permission_group(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.get_or_create(name='Read-Only API')


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0050_auto_20170914_1510'),
    ]

    operations = [
        migrations.RunPython(
            add_permission_group, reverse_code=remove_permission_group),
    ]
