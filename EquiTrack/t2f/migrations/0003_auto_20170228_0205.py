# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-02-28 00:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('t2f', '0002_auto_20170221_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='costassignment',
            name='fund',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='publics.Fund'),
        ),
        migrations.AlterField(
            model_name='costassignment',
            name='grant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='publics.Grant'),
        ),
        migrations.AlterField(
            model_name='costassignment',
            name='wbs',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='publics.WBS'),
        ),
        migrations.AlterField(
            model_name='invoiceitem',
            name='fund',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='publics.Fund'),
        ),
        migrations.AlterField(
            model_name='invoiceitem',
            name='grant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='publics.Grant'),
        ),
        migrations.AlterField(
            model_name='invoiceitem',
            name='wbs',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='publics.WBS'),
        ),
    ]
