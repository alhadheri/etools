# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-04-23 15:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20180419_2113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='staff_id',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='Staff ID'),
        ),
    ]
