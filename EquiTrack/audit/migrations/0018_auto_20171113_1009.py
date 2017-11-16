# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-11-13 10:09
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.jsonb
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('audit', '0017_auto_20171031_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='engagement',
            name='shared_ip_with',
            field=models.CharField(blank=True, choices=[('DPKO', 'DPKO'), ('ECA', 'ECA'), ('ECLAC', 'ECLAC'), ('ESCWA', 'ESCWA'), ('FAO', 'FAO'), ('ILO', 'ILO'), ('IOM', 'IOM'), ('OHCHR', 'OHCHR'), ('UN', 'UN'), ('UN Women', 'UN Women'), ('UNAIDS', 'UNAIDS'), ('UNDP', 'UNDP'), ('UNESCO', 'UNESCO'), ('UNFPA', 'UNFPA'), ('UN - Habitat', 'UN - Habitat'), ('UNHCR', 'UNHCR'), ('UNODC', 'UNODC'), ('UNOPS', 'UNOPS'), ('UNRWA', 'UNRWA'), ('UNSC', 'UNSC'), ('UNU', 'UNU'), ('WB', 'WB'), ('WFP', 'WFP'), ('WHO', 'WHO')], max_length=20, verbose_name='Shared IP with'),
        ),
        migrations.AlterModelOptions(
            name='auditorfirm',
            options={'verbose_name': 'Organization', 'verbose_name_plural': 'Organizations'},
        ),
        migrations.AlterModelOptions(
            name='auditorstaffmember',
            options={'verbose_name': 'Staff Member', 'verbose_name_plural': 'Staff Members'},
        ),
        migrations.AlterField(
            model_name='audit',
            name='audit_observation',
            field=models.TextField(blank=True, verbose_name='Audit Observation'),
        ),
        migrations.AlterField(
            model_name='audit',
            name='audit_opinion',
            field=models.CharField(blank=True, choices=[('unqualified', 'Unqualified'), ('qualified', 'Qualified'), ('disclaimer_opinion', 'Disclaimer opinion'), ('adverse_opinion', 'Adverse opinion')], max_length=20, null=True, verbose_name='Audit Opinion'),
        ),
        migrations.AlterField(
            model_name='audit',
            name='audited_expenditure',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='Audited Expenditure $'),
        ),
        migrations.AlterField(
            model_name='audit',
            name='financial_findings',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='Financial Findings $'),
        ),
        migrations.AlterField(
            model_name='audit',
            name='percent_of_audited_expenditure',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)], verbose_name='% Of Audited Expenditure'),
        ),
        migrations.AlterField(
            model_name='audit',
            name='recommendation',
            field=models.TextField(blank=True, verbose_name='Recommendation'),
        ),
        migrations.AlterField(
            model_name='auditorfirm',
            name='blocked',
            field=models.BooleanField(default=False, verbose_name='Blocked'),
        ),
        migrations.AlterField(
            model_name='auditorfirm',
            name='city',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='auditorfirm',
            name='country',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Country'),
        ),
        migrations.AlterField(
            model_name='auditorfirm',
            name='email',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='auditorfirm',
            name='hidden',
            field=models.BooleanField(default=False, verbose_name='Hidden'),
        ),
        migrations.AlterField(
            model_name='auditorfirm',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Vendor Name'),
        ),
        migrations.AlterField(
            model_name='auditorfirm',
            name='phone_number',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='Phone Number'),
        ),
        migrations.AlterField(
            model_name='auditorfirm',
            name='postal_code',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='Postal Code'),
        ),
        migrations.AlterField(
            model_name='auditorfirm',
            name='street_address',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='auditorfirm',
            name='vendor_number',
            field=models.CharField(blank=True, max_length=30, null=True, unique=True, verbose_name='Vendor Number'),
        ),
        migrations.AlterField(
            model_name='auditorstaffmember',
            name='auditor_firm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='staff_members', to='audit.AuditorFirm', verbose_name='Auditor'),
        ),
        migrations.AlterField(
            model_name='auditorstaffmember',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='audit_auditorstaffmember', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='detailedfindinginfo',
            name='finding',
            field=models.TextField(verbose_name='Description of Finding'),
        ),
        migrations.AlterField(
            model_name='detailedfindinginfo',
            name='micro_assesment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='findings', to='audit.MicroAssessment', verbose_name='Micro Assessment'),
        ),
        migrations.AlterField(
            model_name='detailedfindinginfo',
            name='recommendation',
            field=models.TextField(verbose_name='Recommendation and IP Management Response'),
        ),
        migrations.AlterField(
            model_name='engagement',
            name='additional_supporting_documentation_provided',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='Additional Supporting Documentation Provided'),
        ),
        migrations.AlterField(
            model_name='engagement',
            name='agreement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='audit.PurchaseOrder', verbose_name='Purchase Order'),
        ),
        migrations.AlterField(
            model_name='engagement',
            name='amount_refunded',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='Amount Refunded'),
        ),
        migrations.AlterField(
            model_name='engagement',
            name='authorized_officers',
            field=models.ManyToManyField(blank=True, related_name='engagement_authorizations', to='partners.PartnerStaffMember', verbose_name='Authorized Officers'),
        ),
        migrations.AlterField(
            model_name='engagement',
            name='cancel_comment',
            field=models.TextField(blank=True, verbose_name='Cancel Comment'),
        ),
        migrations.AlterField(
            model_name='engagement',
            name='date_of_cancel',
            field=models.DateField(blank=True, null=True, verbose_name='Date Report Cancelled'),
        ),
        migrations.AlterField(
            model_name='engagement',
            name='date_of_comments_by_ip',
            field=models.DateField(blank=True, null=True, verbose_name='Date Comments Received from IP'),
        ),
        migrations.AlterField(
            model_name='engagement',
            name='date_of_comments_by_unicef',
            field=models.DateField(blank=True, null=True, verbose_name='Date Comments Received from UNICEF'),
        ),
        migrations.AlterField(
            model_name='engagement',
            name='date_of_draft_report_to_ip',
            field=models.DateField(blank=True, null=True, verbose_name='Date Draft Report Issued to IP'),
        ),
        migrations.AlterField(
            model_name='engagement',
            name='date_of_draft_report_to_unicef',
            field=models.DateField(blank=True, null=True, verbose_name='Date Draft Report Issued to UNICEF'),
        ),
        migrations.AlterField(
            model_name='engagement',
            name='date_of_field_visit',
            field=models.DateField(blank=True, null=True, verbose_name='Date of Field Visit'),
        ),
        migrations.AlterField(
            model_name='engagement',
            name='date_of_final_report',
            field=models.DateField(blank=True, null=True, verbose_name='Date Report Finalized'),
        ),
        migrations.AlterField(
            model_name='engagement',
            name='date_of_report_submit',
            field=models.DateField(blank=True, null=True, verbose_name='Date Report Submitted'),
        ),
        migrations.AlterField(
            model_name='engagement',
            name='end_date',
            field=models.DateField(blank=True, null=True, verbose_name='Period End Date'),
        ),
        migrations.AlterField(
            model_name='engagement',
            name='engagement_type',
            field=models.CharField(choices=[('audit', 'Audit'), ('ma', 'Micro Assessment'), ('sc', 'Spot Check'), ('sa', 'Special Audit')], max_length=10, verbose_name='Engagement Type'),
        ),
        migrations.AlterField(
            model_name='engagement',
            name='justification_provided_and_accepted',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='Justification Provided and Accepted'),
        ),
        migrations.AlterField(
            model_name='engagement',
            name='partner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partners.PartnerOrganization', verbose_name='Partner'),
        ),
        migrations.AlterField(
            model_name='engagement',
            name='staff_members',
            field=models.ManyToManyField(to='audit.AuditorStaffMember', verbose_name='Staff Members'),
        ),
        migrations.AlterField(
            model_name='engagement',
            name='start_date',
            field=models.DateField(blank=True, null=True, verbose_name='Period Start Date'),
        ),
        migrations.AlterField(
            model_name='engagement',
            name='status',
            field=django_fsm.FSMField(choices=[('partner_contacted', 'IP Contacted'), ('report_submitted', 'Report Submitted'), ('final', 'Final Report'), ('cancelled', 'Cancelled')], default='partner_contacted', max_length=30, protected=True, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='engagement',
            name='write_off_required',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='Write Off Required '),
        ),
        migrations.AlterField(
            model_name='engagementactionpoint',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_engagement_action_points', to=settings.AUTH_USER_MODEL, verbose_name='Author'),
        ),
        migrations.AlterField(
            model_name='engagementactionpoint',
            name='comments',
            field=models.TextField(verbose_name='Comments'),
        ),
        migrations.AlterField(
            model_name='engagementactionpoint',
            name='description',
            field=models.CharField(choices=[('Invoice and receive reimbursement of ineligible expenditure', 'Invoice and receive reimbursement of ineligible expenditure'), ('Change cash transfer modality (DCT, reimbursement or direct payment)', 'Change cash transfer modality (DCT, reimbursement or direct payment)'), ('IP to incur and report on additional expenditure', 'IP to incur and report on additional expenditure'), ('Review and amend ICE or budget', 'Review and amend ICE or budget'), ('IP to correct FACE form or Statement of Expenditure', 'IP to correct FACE form or Statement of Expenditure'), ('Schedule a programmatic visit', 'Schedule a programmatic visit'), ('Schedule a follow-up spot check', 'Schedule a follow-up spot check'), ('Schedule an audit', 'Schedule an audit'), ('Block future cash transfers', 'Block future cash transfers'), ('Block or mark vendor for deletion', 'Block or mark vendor for deletion'), ('Escalate to Chief of Operations, Dep Rep, or Rep', 'Escalate to Chief of Operations, Dep Rep, or Rep'), ('Escalate to Investigation', 'Escalate to Investigation'), ('Capacity building / Discussion with partner', 'Capacity building / Discussion with partner'), ('Other', 'Other')], max_length=100, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='engagementactionpoint',
            name='due_date',
            field=models.DateField(verbose_name='Due Date'),
        ),
        migrations.AlterField(
            model_name='engagementactionpoint',
            name='engagement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='action_points', to='audit.Engagement', verbose_name='Engagement'),
        ),
        migrations.AlterField(
            model_name='engagementactionpoint',
            name='person_responsible',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='engagement_action_points', to=settings.AUTH_USER_MODEL, verbose_name='Person Responsible'),
        ),
        migrations.AlterField(
            model_name='financialfinding',
            name='audit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='financial_finding_set', to='audit.Audit', verbose_name='Audit'),
        ),
        migrations.AlterField(
            model_name='financialfinding',
            name='description',
            field=models.TextField(verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='financialfinding',
            name='ip_comments',
            field=models.TextField(blank=True, verbose_name='IP Comments'),
        ),
        migrations.AlterField(
            model_name='financialfinding',
            name='recommendation',
            field=models.TextField(blank=True, verbose_name='Recommendation'),
        ),
        migrations.AlterField(
            model_name='finding',
            name='agreed_action_by_ip',
            field=models.TextField(blank=True, verbose_name='Agreed Action by IP'),
        ),
        migrations.AlterField(
            model_name='finding',
            name='category_of_observation',
            field=models.CharField(choices=[('expenditure_not_for_programme_purposes', 'Expenditure not for programme purposes'), ('expenditure_claimed_but_activities_not_undertaken', 'Expenditure claimed but activities not undertaken'), ('expenditure_exceeds_the_approved_budget_rate_or_amount', 'Expenditure exceeds the approved budget rate or amount'), ('expenditure_not_recorded_in_the_correct_period_or_face_form', 'Expenditure not recorded in the correct period or FACE form'), ('advance_claimed_as_expenditure', 'Advance claimed as expenditure'), ('commitments_treated_as_expenditure', 'Commitments treated as expenditure'), ('signatories_on_face_forms_different_from_ip_agreement', 'Signatories on FACE forms different from those in the IP Agreement'), ('no_supporting_documentation', 'No supporting documentation'), ('insufficient_supporting_documentation', 'Insufficient supporting documentation'), ('no_proof_of_payment', 'No proof of payment'), ('no_proof_of_goods_received', 'No proof of goods / services received'), ('poor_record_keeping', 'Poor record keeping'), ('lack_of_audit_trail', 'Lack of audit trail (FACE forms do not reconcile with IPs and UNICEF\u2019s accounting records)'), ('lack_of_bank_reconciliations', 'Lack of bank reconciliations'), ('lack_of_segregation_of_duties', 'Lack of segregation of duties'), ('vat_incorrectly_claimed', 'VAT incorrectly claimed'), ('ineligible_salary_cost', 'Ineligible salary cost'), ('dsa_rates_exceeded', 'DSA rates exceeded'), ('support_costs_incorrectly_calculated', 'Support costs incorrectly calculated'), ('no_competitive_procedures_for_the_award_of_contracts', 'No competitive procedures for the award of contracts'), ('supplier\u2019s_invoices_not_approved', 'Supplier\u2019s invoices not approved'), ('no_evaluation_of_goods_received', 'No evaluation of goods received'), ('lack_of_procedures_for_verification_of_assets', 'Lack of procedures for verification of assets'), ('goods_/_assets_not_used_for_the_intended_purposes', 'Goods / Assets not used for the intended purposes'), ('lack_of_written_agreement_between_ip_and_sub-contractee', 'Lack of written agreement between IP and sub-contractee'), ('lack_of_sub-contractee_financial', 'Lack of sub-contractee financial / substantive progress reporting on file'), ('failure_to_implement_prior_assurance_activity_recommendations', 'Failure to implement prior assurance activity recommendations'), ('other', 'Other')], max_length=100, verbose_name='Category of Observation'),
        ),
        migrations.AlterField(
            model_name='finding',
            name='deadline_of_action',
            field=models.DateField(blank=True, null=True, verbose_name='Deadline of Action'),
        ),
        migrations.AlterField(
            model_name='finding',
            name='priority',
            field=models.CharField(choices=[('high', 'High'), ('low', 'Low')], max_length=4, verbose_name='Priority'),
        ),
        migrations.AlterField(
            model_name='finding',
            name='recommendation',
            field=models.TextField(blank=True, verbose_name='Recommendation'),
        ),
        migrations.AlterField(
            model_name='finding',
            name='spot_check',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='findings', to='audit.SpotCheck', verbose_name='Spot Check'),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='auditor_firm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchase_orders', to='audit.AuditorFirm', verbose_name='Auditor'),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='order_number',
            field=models.CharField(blank=True, max_length=30, null=True, unique=True, verbose_name='Purchase Order Number'),
        ),
        migrations.AlterField(
            model_name='purchaseorderitem',
            name='purchase_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='audit.PurchaseOrder', verbose_name='Purchase Order'),
        ),
        migrations.AlterField(
            model_name='risk',
            name='blueprint',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='risks', to='audit.RiskBluePrint', verbose_name='Blueprint'),
        ),
        migrations.AlterField(
            model_name='risk',
            name='engagement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='risks', to='audit.Engagement', verbose_name='Engagement'),
        ),
        migrations.AlterField(
            model_name='risk',
            name='extra',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='Extra'),
        ),
        migrations.AlterField(
            model_name='risk',
            name='value',
            field=models.SmallIntegerField(blank=True, choices=[(0, 'N/A'), (1, 'Low'), (2, 'Medium'), (3, 'Significant'), (4, 'High')], null=True, verbose_name='Value'),
        ),
        migrations.AlterField(
            model_name='riskblueprint',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blueprints', to='audit.RiskCategory', verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='riskblueprint',
            name='description',
            field=models.TextField(blank=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='riskblueprint',
            name='header',
            field=models.TextField(verbose_name='Header'),
        ),
        migrations.AlterField(
            model_name='riskblueprint',
            name='is_key',
            field=models.BooleanField(default=False, verbose_name='Is Key'),
        ),
        migrations.AlterField(
            model_name='riskblueprint',
            name='weight',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Weight'),
        ),
        migrations.AlterField(
            model_name='riskcategory',
            name='category_type',
            field=models.CharField(choices=[('default', 'Default'), ('primary', 'Primary')], default='default', max_length=20, verbose_name='Category Type'),
        ),
        migrations.AlterField(
            model_name='riskcategory',
            name='code',
            field=models.CharField(blank=True, max_length=20, verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='riskcategory',
            name='header',
            field=models.CharField(max_length=255, verbose_name='Header'),
        ),
        migrations.AlterField(
            model_name='riskcategory',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='audit.RiskCategory', verbose_name='Parent'),
        ),
        migrations.AlterField(
            model_name='spotcheck',
            name='total_amount_of_ineligible_expenditure',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='Total Amount of Ineligible Expenditure'),
        ),
        migrations.AlterField(
            model_name='spotcheck',
            name='total_amount_tested',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='Total Amount Tested'),
        ),
        migrations.AlterField(
            model_name='spotcheck',
            name='internal_controls',
            field=models.TextField(blank=True, verbose_name='Internal Controls'),
        ),
    ]
