
import json
from datetime import date, datetime
from decimal import Decimal

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models import Count, Sum
from django.db.models.functions import Coalesce
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel

from etools.applications.EquiTrack.encoders import EToolsEncoder
from etools.applications.audit.models import Audit, Engagement, MicroAssessment, SpecialAudit, SpotCheck
from etools.applications.EquiTrack.utils import get_current_year
from etools.applications.partners.models import PartnerOrganization, PartnerType


class HactHistory(TimeStampedModel):

    partner = models.ForeignKey(
        PartnerOrganization, verbose_name=_('Partner'), related_name='related_partner',
        on_delete=models.CASCADE,
    )
    year = models.IntegerField(default=get_current_year, verbose_name=_('Year'))
    partner_values = JSONField(null=True, blank=True, verbose_name=_('Partner Values'))

    class Meta:
        unique_together = ('partner', 'year')
        verbose_name_plural = _('Hact Histories')


class AggregateHact(TimeStampedModel):

    year = models.IntegerField(default=get_current_year, unique=True, verbose_name=_('Year'))
    partner_values = JSONField(null=True, blank=True, verbose_name=_('Partner Values'))

    def update(self):
        self.partner_values = json.dumps({
            'assurance_activities': self.get_assurance_activities(),
            'assurance_coverage': self.get_assurance_coverage(),
            'financial_findings': self.get_financial_findings(),
            'financial_findings_numbers': self.get_financial_findings_numbers(),
            'charts': {
                'cash_transfers_amounts': self.cash_transfers_amounts(),
                'cash_transfers_risk_ratings': self.get_cash_transfer_risk_rating(),
                'cash_transfers_partner_type': self.get_cash_transfer_partner_type(),
                'spot_checks_completed': self.get_spot_checks_completed(),
            },
        }, cls=EToolsEncoder)
        self.save()

    @staticmethod
    def get_queryset():
        return PartnerOrganization.objects.active()

    def _sum_json_values(self, qs_filters, filter_dict={}):
        partners = self.get_queryset().filter(**filter_dict)

        def get_value(obj, qs_filters):
            qs_filters = qs_filters.split('__')
            json_field_name = qs_filters.pop(0)
            json_field = getattr(obj, json_field_name)
            json_field = json_field if type(json_field) is dict else json.loads(json_field)
            for qs_filter in qs_filters:
                json_field = json_field[qs_filter]
            return json_field

        return sum([get_value(p, qs_filters) for p in partners])

    def cash_transfers_amounts(self):
        FIRST_LEVEL = Decimal(50000.00)
        SECOND_LEVEL = Decimal(100000.00)
        THIRD_LEVEL = Decimal(350000.00)
        FOURTH_LEVEL = Decimal(500000.00)

        ct_amount_first = self.get_queryset().filter(total_ct_ytd__lte=FIRST_LEVEL)
        cash_transfers_amounts_first = [
            '$0-50,000',
            ct_amount_first.filter(rating=PartnerOrganization.RATING_NON_ASSESSED).aggregate(
                total=Coalesce(Sum('total_ct_ytd'), 0))['total'],
            ct_amount_first.filter(rating=PartnerOrganization.RATING_LOW).aggregate(
                total=Coalesce(Sum('total_ct_ytd'), 0))['total'],
            ct_amount_first.filter(rating=PartnerOrganization.RATING_MODERATE).aggregate(
                total=Coalesce(Sum('total_ct_ytd'), 0))['total'],
            ct_amount_first.filter(rating=PartnerOrganization.RATING_SIGNIFICANT).aggregate(
                total=Coalesce(Sum('total_ct_ytd'), 0))['total'],
            ct_amount_first.filter(rating=PartnerOrganization.RATING_HIGH).aggregate(
                total=Coalesce(Sum('total_ct_ytd'), 0))['total'],
            ct_amount_first.aggregate(count=Count('total_ct_ytd'))['count'],
        ]

        ct_amount_second = self.get_queryset().filter(total_ct_ytd__gt=FIRST_LEVEL, total_ct_ytd__lte=SECOND_LEVEL)
        cash_transfers_amounts_second = [
            '$50,001-100,000',
            ct_amount_second.filter(rating=PartnerOrganization.RATING_NON_ASSESSED).aggregate(
                total=Coalesce(Sum('total_ct_ytd'), 0))['total'],
            ct_amount_second.filter(rating=PartnerOrganization.RATING_LOW).aggregate(
                total=Coalesce(Sum('total_ct_ytd'), 0))['total'],
            ct_amount_second.filter(rating=PartnerOrganization.RATING_MODERATE).aggregate(
                total=Coalesce(Sum('total_ct_ytd'), 0))['total'],
            ct_amount_second.filter(rating=PartnerOrganization.RATING_SIGNIFICANT).aggregate(
                total=Coalesce(Sum('total_ct_ytd'), 0))['total'],
            ct_amount_second.filter(rating=PartnerOrganization.RATING_HIGH).aggregate(
                total=Coalesce(Sum('total_ct_ytd'), 0))['total'],
            ct_amount_second.aggregate(count=Count('total_ct_ytd'))['count'],
        ]

        ct_amount_third = self.get_queryset().filter(total_ct_ytd__gt=SECOND_LEVEL, total_ct_ytd__lte=THIRD_LEVEL)
        cash_transfers_amounts_third = [
            '$100,001-350,000',
            ct_amount_third.filter(rating=PartnerOrganization.RATING_NON_ASSESSED).aggregate(
                total=Coalesce(Sum('total_ct_ytd'), 0))['total'],
            ct_amount_third.filter(rating=PartnerOrganization.RATING_LOW).aggregate(
                total=Coalesce(Sum('total_ct_ytd'), 0))['total'],
            ct_amount_third.filter(rating=PartnerOrganization.RATING_MODERATE).aggregate(
                total=Coalesce(Sum('total_ct_ytd'), 0))['total'],
            ct_amount_third.filter(rating=PartnerOrganization.RATING_SIGNIFICANT).aggregate(
                total=Coalesce(Sum('total_ct_ytd'), 0))['total'],
            ct_amount_third.filter(rating=PartnerOrganization.RATING_HIGH).aggregate(
                total=Coalesce(Sum('total_ct_ytd'), 0))['total'],
            ct_amount_third.aggregate(count=Count('total_ct_ytd'))['count'],
        ]

        ct_amount_fourth = self.get_queryset().filter(total_ct_ytd__gt=THIRD_LEVEL, total_ct_ytd__lte=FOURTH_LEVEL)
        cash_transfers_amounts_fourth = [
            '$350,001-500,000',
            ct_amount_fourth.filter(rating=PartnerOrganization.RATING_NON_ASSESSED).aggregate(
                total=Coalesce(Sum('total_ct_ytd'), 0))['total'],
            ct_amount_fourth.filter(rating=PartnerOrganization.RATING_LOW).aggregate(
                total=Coalesce(Sum('total_ct_ytd'), 0))['total'],
            ct_amount_fourth.filter(rating=PartnerOrganization.RATING_MODERATE).aggregate(
                total=Coalesce(Sum('total_ct_ytd'), 0))['total'],
            ct_amount_fourth.filter(rating=PartnerOrganization.RATING_SIGNIFICANT).aggregate(
                total=Coalesce(Sum('total_ct_ytd'), 0))['total'],
            ct_amount_fourth.filter(rating=PartnerOrganization.RATING_HIGH).aggregate(
                total=Coalesce(Sum('total_ct_ytd'), 0))['total'],
            ct_amount_fourth.aggregate(count=Count('total_ct_ytd'))['count'],
        ]

        ct_amount_fifth = self.get_queryset().filter(total_ct_ytd__gt=FOURTH_LEVEL)
        cash_transfers_amounts_fifth = [
            '>$500,000',
            ct_amount_fifth.filter(rating=PartnerOrganization.RATING_NON_ASSESSED).aggregate(
                total=Coalesce(Sum('total_ct_ytd'), 0))['total'],
            ct_amount_fifth.filter(rating=PartnerOrganization.RATING_LOW).aggregate(
                total=Coalesce(Sum('total_ct_ytd'), 0))['total'],
            ct_amount_fifth.filter(rating=PartnerOrganization.RATING_MODERATE).aggregate(
                total=Coalesce(Sum('total_ct_ytd'), 0))['total'],
            ct_amount_fifth.filter(rating=PartnerOrganization.RATING_SIGNIFICANT).aggregate(
                total=Coalesce(Sum('total_ct_ytd'), 0))['total'],
            ct_amount_fifth.filter(rating=PartnerOrganization.RATING_HIGH).aggregate(
                total=Coalesce(Sum('total_ct_ytd'), 0))['total'],
            ct_amount_fifth.aggregate(count=Count('total_ct_ytd'))['count'],
        ]

        return [
            ['Risk Rating', 'Not Required', 'Low', 'Medium', 'Significant', 'High', 'Number of IPs'],
            cash_transfers_amounts_first,
            cash_transfers_amounts_second,
            cash_transfers_amounts_third,
            cash_transfers_amounts_fourth,
            cash_transfers_amounts_fifth,
        ]

    def get_cash_transfer_risk_rating(self):
        total_ct_dict = {
            'total': Sum('total_ct_ytd'),
            'count': Count('total_ct_ytd')
        }

        high = self.get_queryset().filter(rating=PartnerOrganization.RATING_HIGH).aggregate(**total_ct_dict)
        significant = self.get_queryset().filter(
            rating=PartnerOrganization.RATING_SIGNIFICANT).aggregate(**total_ct_dict)
        moderate = self.get_queryset().filter(rating=PartnerOrganization.RATING_MODERATE).aggregate(**total_ct_dict)
        low = self.get_queryset().filter(rating=PartnerOrganization.RATING_LOW).aggregate(**total_ct_dict)
        non_assessed = self.get_queryset().filter(
            rating=PartnerOrganization.RATING_NON_ASSESSED).aggregate(**total_ct_dict)

        return [
            ['Risk Rating', 'Total Cash Transfers', {'role': 'style'}, 'Number of IPs'],
            ['Not Required', non_assessed['total'], '#D8D8D8', non_assessed['count']],
            ['Low', low['total'], '#2BB0F2', low['count']],
            ['Medium', moderate['total'], '#FECC02', moderate['count']],
            ['Significant', significant['total'], '#F05656', significant['count']],
            ['High', high['total'], '#751010', high['count']],
        ]

    def get_cash_transfer_partner_type(self):
        total_ct_dict = {
            'total': Sum('total_ct_ytd'),
            'count': Count('total_ct_ytd')
        }

        gov = self.get_queryset().filter(partner_type=PartnerType.GOVERNMENT).aggregate(**total_ct_dict)
        cso = self.get_queryset().filter(
            partner_type=PartnerType.CIVIL_SOCIETY_ORGANIZATION).aggregate(**total_ct_dict)

        return [
            ['Partner Type', 'Total Cash Transfers', {'role': 'style'}, 'Number of Partners'],
            ['CSO', cso['total'], '#FECC02', cso['count']],
            ['GOV', gov['total'], '#F05656', gov['count']],
        ]

    @staticmethod
    def get_spot_checks_completed():
        qs = SpotCheck.objects.filter(status=Engagement.FINAL, date_of_draft_report_to_unicef__year=datetime.now().year)
        return [
            ['Completed by', 'Count'],
            ['Staff', qs.filter(partner__vendor_number='0000000000').count()],
            ['Service Providers', qs.exclude(partner__vendor_number='0000000000').count()],
        ]

    def get_assurance_activities(self):
        year_limit = date.today().year - PartnerOrganization.EXPIRING_ASSESSMENT_LIMIT_YEAR
        return {
            'programmatic_visits': {
                'completed': self._sum_json_values('hact_values__programmatic_visits__completed__total'),
                'min_required': sum([p.min_req_programme_visits for p in self.get_queryset()]),
            },
            'spot_checks': {
                'completed': self._sum_json_values('hact_values__spot_checks__completed__total'),
                'min_required': sum([p.min_req_spot_checks for p in self.get_queryset()]),
                'follow_up': self.get_queryset().aggregate(total=Coalesce(Sum(
                    'planned_engagement__spot_check_follow_up'), 0))['total']
            },
            'scheduled_audit': Audit.objects.filter(
                status=Engagement.FINAL, date_of_draft_report_to_unicef__year=datetime.now().year).count(),
            'special_audit': SpecialAudit.objects.filter(
                status=Engagement.FINAL, date_of_draft_report_to_unicef__year=datetime.now().year).count(),
            'micro_assessment': MicroAssessment.objects.filter(
                status=Engagement.FINAL, date_of_draft_report_to_unicef__year=datetime.now().year).count(),
            'missing_micro_assessment': PartnerOrganization.objects.active(
                last_assessment_date__isnull=False, last_assessment_date__year__lte=year_limit).count(),
        }

    @staticmethod
    def get_financial_findings():
        refunds = Audit.objects.filter(amount_refunded__isnull=False, status=Engagement.FINAL,
                                       date_of_draft_report_to_unicef__year=datetime.now().year).aggregate(
            total=Coalesce(Sum('amount_refunded'), 0))['total']
        additional_supporting_document_provided = Audit.objects.filter(
            date_of_draft_report_to_unicef__year=datetime.now().year,
            additional_supporting_documentation_provided__isnull=False,
            status=Engagement.FINAL).aggregate(
            total=Coalesce(Sum('additional_supporting_documentation_provided'), 0))['total']
        justification_provided_and_accepted = Audit.objects.filter(
            date_of_draft_report_to_unicef__year=datetime.now().year,
            status=Engagement.FINAL,
            justification_provided_and_accepted__isnull=False).aggregate(
            total=Coalesce(Sum('justification_provided_and_accepted'), 0))['total']
        impairment = Audit.objects.filter(
            status=Engagement.FINAL,
            write_off_required__isnull=False,
            date_of_draft_report_to_unicef__year=datetime.now().year).aggregate(
            total=Coalesce(Sum('write_off_required'), 0))['total']

        # pending_unsupported_amount property
        outstanding_audits = Audit.objects.filter(status=Engagement.FINAL,
                                                  date_of_draft_report_to_unicef__year=datetime.now().year)
        _ff = outstanding_audits.filter(financial_findings__isnull=False).aggregate(
            total=Coalesce(Sum('financial_findings'), 0))['total']
        _ar = outstanding_audits.filter(amount_refunded__isnull=False).aggregate(
            total=Coalesce(Sum('amount_refunded'), 0))['total']
        _asdp = outstanding_audits.filter(additional_supporting_documentation_provided__isnull=False).aggregate(
            total=Coalesce(Sum('additional_supporting_documentation_provided'), 0))['total']
        _wor = outstanding_audits.filter(write_off_required__isnull=False).aggregate(
            total=Coalesce(Sum('write_off_required'), 0))['total']
        outstanding = _ff - _ar - _asdp - _wor

        total_financial_findings = Audit.objects.filter(
            date_of_draft_report_to_unicef__year=datetime.now().year,
            financial_findings__isnull=False,
            status=Engagement.FINAL).aggregate(
            total=Coalesce(Sum('financial_findings'), 0))['total']
        total_audited_expenditure = Audit.objects.filter(
            date_of_draft_report_to_unicef__year=datetime.now().year,
            audited_expenditure__isnull=False,
            status=Engagement.FINAL).aggregate(
            total=Coalesce(Sum('audited_expenditure'), 0))['total']

        return [
            {
                'name': 'Total Audited Expenditure',
                'value': total_audited_expenditure,
                'highlighted': False,
            },
            {
                'name': 'Total Financial Findings',
                'value': total_financial_findings,
                'highlighted': True,
            },
            {
                'name': 'Refunds',
                'value': refunds,
                'highlighted': False,
            },
            {
                'name': 'Additional Supporting Documentation Received',
                'value': additional_supporting_document_provided,
                'highlighted': False,
            },
            {
                'name': 'Justification Provided and Accepted',
                'value': justification_provided_and_accepted,
                'highlighted': False,
            },
            {
                'name': 'Impairment',
                'value': impairment,
                'highlighted': False,
            },
            {
                'name': 'Outstanding(Requires Follow-up)',
                'value': outstanding,
                'highlighted': True,
            }
        ]

    @staticmethod
    def get_financial_findings_numbers():
        return [
            {
                'name': 'Number of High Priority Findings',
                'value': Audit.objects.filter(risks__value=4, status=Engagement.FINAL,
                                              date_of_draft_report_to_unicef__year=datetime.now().year).count(),
            },
            {
                'name': 'Number of Medium Priority Findings',
                'value': Audit.objects.filter(risks__value=2, status=Engagement.FINAL,
                                              date_of_draft_report_to_unicef__year=datetime.now().year).count(),
            },
            {
                'name': 'Number of Low Priority Findings',
                'value': Audit.objects.filter(risks__value=1, status=Engagement.FINAL,
                                              date_of_draft_report_to_unicef__year=datetime.now().year).count(),
            },
            {
                'name': 'Audit Opinion',
                'value': [
                    {
                        'name': 'qualified',
                        'value': Audit.objects.filter(audit_opinion=Audit.OPTION_QUALIFIED, status=Engagement.FINAL,
                                                      date_of_draft_report_to_unicef__year=datetime.now().year).count(),
                    },
                    {
                        'name': 'unqualified',
                        'value': Audit.objects.filter(audit_opinion=Audit.OPTION_UNQUALIFIED, status=Engagement.FINAL,
                                                      date_of_draft_report_to_unicef__year=datetime.now().year).count(),
                    },
                    {
                        'name': 'denial',
                        'value': Audit.objects.filter(audit_opinion=Audit.OPTION_DENIAL, status=Engagement.FINAL,
                                                      date_of_draft_report_to_unicef__year=datetime.now().year).count(),
                    },
                    {
                        'name': 'adverse',
                        'value': Audit.objects.filter(audit_opinion=Audit.OPTION_ADVERSE, status=Engagement.FINAL,
                                                      date_of_draft_report_to_unicef__year=datetime.now().year).count(),
                    },
                ],
            }
        ]

    @staticmethod
    def get_assurance_coverage():
        qs = PartnerOrganization.objects.active()

        no_coverage = qs.filter(hact_values__assurance_coverage=PartnerOrganization.ASSURANCE_VOID)
        partial_coverage = qs.filter(hact_values__assurance_coverage=PartnerOrganization.ASSURANCE_PARTIAL)
        full_coverage = qs.filter(hact_values__assurance_coverage=PartnerOrganization.ASSURANCE_COMPLETE)
        return {
            'coverage_by_number_of_ips': [
                ['Coverage by number of IPs', 'Count'],
                ['Without Assurance', no_coverage.count()],
                ['Partially Met Requirements', partial_coverage.count()],
                ['Met Requirements', full_coverage.count()]
            ],
            'coverage_by_cash_transfer': [
                ['Coverage by Cash Transfer (USD) (Total)', 'Count'],
                ['Without Assurance', no_coverage.aggregate(total=Coalesce(Sum('total_ct_ytd'), 0))['total']],
                ['Partially Met Requirements', partial_coverage.aggregate(
                    total=Coalesce(Sum('total_ct_ytd'), 0))['total']],
                ['Met Requirements', full_coverage.aggregate(total=Coalesce(Sum('total_ct_ytd'), 0))['total']],

            ],
            'table': [
                {
                    'label': 'Active Partners',
                    'value': PartnerOrganization.objects.active().count()
                },
                {
                    'label': 'IPs without required PV',
                    'value': PartnerOrganization.objects.not_programmatic_visit_compliant().count()
                },
                {
                    'label': 'IPs without required SC',
                    'value': PartnerOrganization.objects.not_spot_check_compliant().count()
                },
                {
                    'label': 'IPs without required assurance',
                    'value': PartnerOrganization.objects.not_assurance_compliant().count()
                }
            ]
        }
