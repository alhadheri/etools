# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-12-06 11:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('audit', '0020_auto_20171206_1103'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auditorstaffmember',
            name='auditor_firm',
        ),
        migrations.RemoveField(
            model_name='auditorstaffmember',
            name='user',
        ),
        migrations.RemoveField(
            model_name='purchaseorder',
            name='auditor_firm',
        ),
        migrations.AlterUniqueTogether(
            name='purchaseorderitem',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='purchaseorderitem',
            name='purchase_order',
        ),
        migrations.RemoveField(
            model_name='engagement',
            name='agreement',
        ),
        migrations.RemoveField(
            model_name='engagement',
            name='po_item',
        ),
        migrations.RemoveField(
            model_name='engagement',
            name='staff_members',
        ),
        migrations.DeleteModel(
            name='AuditorFirm',
        ),
        migrations.DeleteModel(
            name='AuditorStaffMember',
        ),
        migrations.DeleteModel(
            name='PurchaseOrder',
        ),
        migrations.DeleteModel(
            name='PurchaseOrderItem',
        ),
        migrations.RenameField(
            model_name='engagement',
            old_name='agreement1',
            new_name='agreement',
        ),
        migrations.RenameField(
            model_name='engagement',
            old_name='po_item1',
            new_name='po_item',
        ),
        migrations.RenameField(
            model_name='engagement',
            old_name='staff_members1',
            new_name='staff_members',
        ),
        migrations.AlterField(
            model_name='engagement',
            name='agreement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchase_order.PurchaseOrder',
                                    verbose_name='Purchase Order'),
        ),
        migrations.AlterField(
            model_name='engagement',
            name='staff_members',
            field=models.ManyToManyField(to='purchase_order.AuditorStaffMember', verbose_name='Staff Members'),
        ),
    ]
