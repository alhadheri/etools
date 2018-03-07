# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-02-28 17:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0064_remove_partnerorganization_shared_partner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='interventionplannedvisits',
            old_name='programmatic',
            new_name='programmatic_q4',
        ),
        migrations.AddField(
            model_name='interventionplannedvisits',
            name='programmatic_q1',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='interventionplannedvisits',
            name='programmatic_q2',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='interventionplannedvisits',
            name='programmatic_q3',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterUniqueTogether(
            name='interventionplannedvisits',
            unique_together=set([('intervention', 'year')]),
        ),
        migrations.RemoveField(
            model_name='interventionplannedvisits',
            name='quarter',
        ),
    ]
