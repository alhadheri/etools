# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-24 18:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('t2f', '0003_make_not_nullable'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='invoice',
            options={'ordering': ['pk']},
        ),
    ]
