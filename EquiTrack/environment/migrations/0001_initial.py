# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-03-26 16:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='IssueCheckConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_id', models.CharField(db_index=True, max_length=100, unique=True, verbose_name='Check id')),
                ('is_active', models.BooleanField(default=False, verbose_name='Is Active')),
            ],
        ),
        migrations.CreateModel(
            name='TenantFlag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The human/computer readable name.', max_length=100, unique=True, verbose_name='Name')),
                ('everyone', models.NullBooleanField(help_text='Flip this flag on (Yes) or off (No) for everyone, overriding all other settings. Leave as Unknown to use normally.', verbose_name='Everyone')),
                ('percent', models.DecimalField(blank=True, decimal_places=1, help_text='A number between 0.0 and 99.9 to indicate a percentage of users for whom this flag will be active.', max_digits=3, null=True, verbose_name='Percent')),
                ('testing', models.BooleanField(default=False, help_text='Allow this flag to be set for a session for user testing.', verbose_name='Testing')),
                ('superusers', models.BooleanField(default=True, help_text='Flag always active for superusers?', verbose_name='Superusers')),
                ('staff', models.BooleanField(default=False, help_text='Flag always active for staff?', verbose_name='Staff')),
                ('authenticated', models.BooleanField(default=False, help_text='Flag always active for authenticate users?', verbose_name='Authenticated')),
                ('languages', models.TextField(blank=True, default='', help_text='Activate this flag for users with one of these languages (comma separated list)', verbose_name='Languages')),
                ('rollout', models.BooleanField(default=False, help_text='Activate roll-out mode?', verbose_name='Rollout')),
                ('note', models.TextField(blank=True, help_text='Note where this Flag is used.', verbose_name='Note')),
                ('created', models.DateTimeField(db_index=True, default=django.utils.timezone.now, help_text='Date when this Flag was created.', verbose_name='Created')),
                ('modified', models.DateTimeField(default=django.utils.timezone.now, help_text='Date when this Flag was last modified.', verbose_name='Modified')),
                ('countries', models.ManyToManyField(blank=True, help_text='Activate this flag for these countries.', to='users.Country', verbose_name='Countries')),
                ('groups', models.ManyToManyField(blank=True, help_text='Activate this flag for these user groups.', to='auth.Group', verbose_name='Users')),
                ('users', models.ManyToManyField(blank=True, help_text='Activate this flag for these users.', to=settings.AUTH_USER_MODEL, verbose_name='Users')),
            ],
            options={
                'verbose_name_plural': 'Flags',
            },
        ),
        migrations.CreateModel(
            name='TenantSwitch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The human/computer readable name.', max_length=100, unique=True, verbose_name='Name')),
                ('active', models.BooleanField(default=False, help_text='Is this switch active?', verbose_name='Active')),
                ('note', models.TextField(blank=True, help_text='Note where this Switch is used.', verbose_name='Note')),
                ('created', models.DateTimeField(db_index=True, default=django.utils.timezone.now, help_text='Date when this Switch was created.', verbose_name='Created')),
                ('modified', models.DateTimeField(default=django.utils.timezone.now, help_text='Date when this Switch was last modified.', verbose_name='Modified')),
                ('countries', models.ManyToManyField(blank=True, help_text='Activate this switch for these countries.', to='users.Country', verbose_name='Countries')),
            ],
            options={
                'verbose_name_plural': 'Switches',
            },
        ),
    ]
