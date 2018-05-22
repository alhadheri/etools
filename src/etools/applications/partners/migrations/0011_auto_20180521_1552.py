# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-21 15:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0010_auto_20180514_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partnerorganization',
            name='rating',
            field=models.CharField(blank=True, choices=[('High', 'High'), ('Significant', 'Significant'), ('Medium', 'Medium'), ('Low', 'Low'), ('Not Required', 'Not Required')], max_length=50, null=True, verbose_name='Risk Rating'),
        ),
    ]
