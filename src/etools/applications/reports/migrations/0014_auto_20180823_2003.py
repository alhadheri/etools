# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-08-23 20:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0013_auto_20180709_1348'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='type',
            field=models.CharField(choices=[('Outcome', 'Outcome'), ('Output', 'Output'), ('Activity', 'Activity')], default='Outcome', max_length=10, verbose_name='Result Type'),
        ),
        migrations.AlterField(
            model_name='result',
            name='result_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reports.ResultType', verbose_name='Result Type'),
        ),
    ]
