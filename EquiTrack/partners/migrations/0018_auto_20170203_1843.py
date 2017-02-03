# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-02-03 16:43
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations
import partners.models


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0017_remove_bankdetails_agreement'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='governmentinterventionresult',
            name='activities_list',
        ),
        migrations.AddField(
            model_name='governmentinterventionresult',
            name='activity',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=partners.models.activity_default, null=True),
        ),
    ]
