# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-03-26 16:05

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models

import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditorFirm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(
                    default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(
                    default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('vendor_number', models.CharField(blank=True, max_length=30,
                                                   null=True, unique=True, verbose_name='Vendor Number')),
                ('name', models.CharField(max_length=255, verbose_name='Vendor Name')),
                ('street_address', models.CharField(blank=True, max_length=500, null=True, verbose_name='Address')),
                ('city', models.CharField(blank=True, max_length=255, null=True, verbose_name='City')),
                ('postal_code', models.CharField(blank=True, max_length=32, null=True, verbose_name='Postal Code')),
                ('country', models.CharField(blank=True, max_length=255, null=True, verbose_name='Country')),
                ('email', models.CharField(blank=True, max_length=255, null=True, verbose_name='Email')),
                ('phone_number', models.CharField(blank=True, max_length=32, null=True, verbose_name='Phone Number')),
                ('vision_synced', models.BooleanField(default=False, verbose_name='Synced from VISION')),
                ('blocked', models.BooleanField(default=False, verbose_name='Blocked in VISION')),
                ('hidden', models.BooleanField(default=False, verbose_name='Hidden')),
                ('deleted_flag', models.BooleanField(default=False, verbose_name='Marked For Deletion in VISION')),
            ],
            options={
                'abstract': False,
                'ordering': ('id',),
                'verbose_name': 'Organization',
                'verbose_name_plural': 'Organizations',
            },
        ),
        migrations.CreateModel(
            name='AuditorStaffMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auditor_firm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                                   related_name='staff_members', to='purchase_order.AuditorFirm', verbose_name='Auditor')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE,
                                              related_name='purchase_order_auditorstaffmember', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'abstract': False,
                'ordering': ('id',),
                'verbose_name': 'Staff Member',
                'verbose_name_plural': 'Staff Members',
            },
        ),
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(
                    default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(
                    default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('order_number', models.CharField(blank=True, max_length=30,
                                                  null=True, unique=True, verbose_name='Purchase Order Number')),
                ('contract_start_date', models.DateField(blank=True, null=True, verbose_name='PO Date')),
                ('contract_end_date', models.DateField(blank=True, null=True, verbose_name='Contract Expiry Date')),
                ('auditor_firm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                                   related_name='purchase_orders', to='purchase_order.AuditorFirm', verbose_name='Auditor')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PurchaseOrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='PO Item Number')),
                ('purchase_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                                     related_name='items', to='purchase_order.PurchaseOrder', verbose_name='Purchase Order')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='purchaseorderitem',
            unique_together=set([('purchase_order', 'number')]),
        ),
    ]