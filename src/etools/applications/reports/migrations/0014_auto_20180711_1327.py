# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-07-11 13:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0013_auto_20180709_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportingrequirement',
            name='end_date',
            field=models.DateField(blank=True, verbose_name='End Date'),
        ),
        migrations.AlterField(
            model_name='reportingrequirement',
            name='start_date',
            field=models.DateField(verbose_name='Start Date'),
        ),
    ]
