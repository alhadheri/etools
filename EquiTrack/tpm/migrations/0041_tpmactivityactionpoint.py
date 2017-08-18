# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-08-17 12:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('locations', '0004_auto_20170112_2051'),
        ('reports', '0012_indicator_active'),
        ('users', '0008_workspacecounter'),
        ('tpm', '0040_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='TPMActivityActionPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('due_date', models.DateTimeField()),
                ('status', models.CharField(choices=[('open', 'Open'), ('ongoing', 'Ongoing'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], max_length=9, null=True, verbose_name='Status')),
                ('description', models.TextField()),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('actions_taken', models.TextField(blank=True, null=True)),
                ('follow_up', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_tpm_activity_action_points', to=settings.AUTH_USER_MODEL)),
                ('cp_outputs', models.ManyToManyField(to='reports.Result', verbose_name='CP Output')),
                ('locations', models.ManyToManyField(to='locations.Location')),
                ('person_responsible', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tpm_activity_action_points', to=settings.AUTH_USER_MODEL)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Section')),
                ('tpm_activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='action_points', to='tpm.TPMActivity')),
            ],
        ),
    ]
