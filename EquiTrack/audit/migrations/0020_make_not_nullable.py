# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2018-02-21 12:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audit', '0019_fix_null_values'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audit',
            name='audit_opinion',
            field=models.CharField(blank=True, choices=[('unqualified', 'Unqualified'), ('qualified', 'Qualified'), ('disclaimer_opinion', 'Disclaimer opinion'), ('adverse_opinion', 'Adverse opinion')], default='', max_length=20, verbose_name='Audit Opinion'),
        ),
        migrations.AlterField(
            model_name='auditorfirm',
            name='city',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='auditorfirm',
            name='country',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Country'),
        ),
        migrations.AlterField(
            model_name='auditorfirm',
            name='email',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='auditorfirm',
            name='phone_number',
            field=models.CharField(blank=True, default='', max_length=32, verbose_name='Phone Number'),
        ),
        migrations.AlterField(
            model_name='auditorfirm',
            name='postal_code',
            field=models.CharField(blank=True, default='', max_length=32, verbose_name='Postal Code'),
        ),
        migrations.AlterField(
            model_name='auditorfirm',
            name='street_address',
            field=models.CharField(blank=True, default='', max_length=500, verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='auditorfirm',
            name='vendor_number',
            field=models.CharField(blank=True, default='', max_length=30, unique=True, verbose_name='Vendor Number'),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='order_number',
            field=models.CharField(blank=True, default='', max_length=30, unique=True, verbose_name='Purchase Order Number'),
        ),
    ]
