# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-08-03 15:45
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission', models.CharField(choices=[('view', 'View'), ('edit', 'Edit'), ('action', 'Action')], max_length=10)),
                ('permission_type', models.CharField(choices=[('allow', 'Allow'), ('disallow', 'Disallow')], default='allow', max_length=10)),
                ('target', models.CharField(max_length=100)),
                ('condition', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), default=[], size=None)),
            ],
        ),
    ]
