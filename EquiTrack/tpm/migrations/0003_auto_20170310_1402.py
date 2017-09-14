# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-03-10 12:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reports', '0007_auto_20170215_1706'),
        ('locations', '0004_auto_20170112_2051'),
        ('partners', '0023_auto_20170301_2324'),
        ('tpm', '0002_auto_20170906_1417'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=b'files')),
                ('object_id', models.IntegerField()),
                ('code', models.CharField(blank=True, max_length=20)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='FileType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TPMLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of_site', models.CharField(blank=True, max_length=255)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locations.Location')),
                ('sectors_covered', models.ManyToManyField(blank=True, to='reports.Sector')),
            ],
        ),
        migrations.CreateModel(
            name='TPMVisit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('visit_start', models.DateField()),
                ('visit_end', models.DateField()),
                ('status', models.CharField(choices=[(b'draft', b'Draft'), (b'submitted', b'Submitted'), (b'tpm_approved', b'TPM Approved'), (b'tpm_rejected', b'TPM Rejected'), (b'unicef_confirmed', b'Confirmed'), (b'tpm_reported', b'TPM Reported'), (b'unicef_approved', b'Approved')], default=b'draft', max_length=20)),
                ('reject_comment', models.TextField(blank=True)),
                ('partnership', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partners.Intervention')),
                ('results', models.ManyToManyField(blank=True, to='partners.InterventionResultLink')),
                ('tpm_partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partners.PartnerOrganization')),
                ('unicef_focal_points', models.ManyToManyField(related_name='tpm_visits', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TPMVisitReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_verify_supply_list', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='TPMVisitReportedIndicator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('indicator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.Indicator')),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tpm.TPMVisitReport')),
            ],
        ),
        migrations.AddField(
            model_name='tpmvisitreport',
            name='selected_indicators',
            field=models.ManyToManyField(through='tpm.TPMVisitReportedIndicator', to='reports.Indicator'),
        ),
        migrations.AddField(
            model_name='tpmvisitreport',
            name='tpm_visit',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='tpm_report', to='tpm.TPMVisit'),
        ),
        migrations.AddField(
            model_name='tpmlocation',
            name='tpm_visit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tpm_locations', to='tpm.TPMVisit'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='file_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tpm.FileType'),
        ),
    ]
