# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-26 21:12
from __future__ import unicode_literals

from django.db import migrations, transaction


@transaction.atomic
def create_planned_engagements(apps, schema_editor):
    PartnerOrganization = apps.get_model('partners', 'PartnerOrganization')
    PlannedEngagement = apps.get_model('partners', 'PlannedEngagement')
    for partner in PartnerOrganization.objects.all():
        PlannedEngagement.objects.get_or_create(partner=partner)


@transaction.atomic
def migrate_shared_partner(apps, schema_editor):
    PartnerOrganization = apps.get_model('partners', 'PartnerOrganization')

    for p in PartnerOrganization.objects.filter(shared_partner='with UNDP').exclude(shared_with__contains=['UNDP',]):
        if not p.shared_with:
            p.shared_with = []
        p.shared_with.append('UNDP')
        p.save()
    for p in PartnerOrganization.objects.filter(shared_partner='with UNFPA').exclude(shared_with__contains=['UNFPA',]):
        if not p.shared_with:
            p.shared_with = []
        p.shared_with.append('UNFPA')
        p.save()
    for p in PartnerOrganization.objects.filter(shared_partner='with UNDP & UNFPA').exclude(shared_with__contains=['UNFPA',]):
        if not p.shared_with:
            p.shared_with = []
        p.shared_with.append('UNFPA')
        p.save()
    for p in PartnerOrganization.objects.filter(shared_partner='with UNDP & UNFPA').exclude(shared_with__contains=['UNDP',]):
        if not p.shared_with:
            p.shared_with = []
        p.shared_with.append('UNDP')
        p.save()


@transaction.atomic
def migrate_planned_visits(apps, schema_editor):
    InterventionPlannedVisits = apps.get_model('partners', 'InterventionPlannedVisits')
    InterventionPlannedVisits.objects.all().update(quarter='q4')


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0062_auto_20180226_2112'),
    ]

    operations = [
        migrations.RunPython(create_planned_engagements, reverse_code=migrations.RunPython.noop),
        migrations.RunPython(migrate_shared_partner, reverse_code=migrations.RunPython.noop),
        migrations.RunPython(migrate_planned_visits, reverse_code=migrations.RunPython.noop)
    ]