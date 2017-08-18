from datetime import timedelta, datetime

from django.core.management import call_command
from django.utils.translation import ugettext as _

from rest_framework import status

from EquiTrack.tests.mixins import APITenantTestCase
from EquiTrack.factories import SectionFactory
from .base import TPMTestCaseMixin
from .factories import TPMVisitFactory, TPMPartnerFactory

from ..models import TPMActivityActionPoint


class TestTPMVisitViewSet(TPMTestCaseMixin, APITenantTestCase):
    def setUp(self):
        super(TestTPMVisitViewSet, self).setUp()
        call_command('update_tpm_permissions', verbosity=0)

    def _test_list_view(self, user, expected_visits):
        response = self.forced_auth_req(
            'get',
            '/api/tpm/visits/',
            user=user
        )

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(
            sorted(map(lambda x: x['id'], response.data['results'])),
            sorted(map(lambda x: x.id, expected_visits))
        )

    def test_list_view(self):
        additional_tpm_visit = TPMVisitFactory()

        self._test_list_view(self.pme_user, [self.tpm_visit, additional_tpm_visit, ])
        self._test_list_view(self.unicef_user, [self.tpm_visit, additional_tpm_visit, ])
        self._test_list_view(self.unicef_focal_point, [self.tpm_visit, additional_tpm_visit, ])

        self._test_list_view(self.tpm_user, [self.tpm_visit, ])

        self._test_list_view(self.usual_user, [])

    def test_create_empty(self):
        create_response = self.forced_auth_req(
            'post',
            '/api/tpm/visits/',
            user=self.pme_user,
            data={}
        )

        self.assertEquals(create_response.status_code, status.HTTP_201_CREATED)

    def test_assign_empty(self):
        create_response = self.forced_auth_req(
            'post',
            '/api/tpm/visits/',
            user=self.pme_user,
            data={}
        )

        self.assertEquals(create_response.status_code, status.HTTP_201_CREATED)

        assign_response = self.forced_auth_req(
            'post',
            '/api/tpm/visits/{}/assign/'.format(create_response.data['id']),
            user=self.pme_user,
            data={}
        )
        self.assertEquals(assign_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('tpm_partner', assign_response.data)
        self.assertEquals(assign_response.data['tpm_partner'], _('This field is required.'))

    def test_assign(self):
        create_response = self.forced_auth_req(
            'post',
            '/api/tpm/visits/',
            user=self.pme_user,
            data={
                'tpm_partner': self.tpm_visit.tpm_partner_id,
                'unicef_focal_points': self.tpm_visit.unicef_focal_points.values_list('id', flat=True),
                'sections': self.tpm_visit.sections.values_list('id', flat=True),
                'tpm_activities': [{
                    'partnership': activity.partnership_id,
                    'cp_output': activity.cp_output_id,
                    'locations': activity.locations.values_list('id', flat=True),
                } for activity in self.tpm_visit.tpm_activities.all()]
            }
        )
        self.assertEquals(create_response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(create_response.data['start_date'], self.tpm_visit.start_date)
        self.assertEqual(create_response.data['end_date'], self.tpm_visit.end_date)

        assign_response = self.forced_auth_req(
            'post',
            '/api/tpm/visits/{}/assign/'.format(create_response.data['id']),
            user=self.pme_user,
            data={}
        )

        self.assertEquals(assign_response.status_code, status.HTTP_200_OK)

    def _approve_visit(self):
        self._do_transition(self.tpm_visit, 'assign', self.pme_user)
        self._do_transition(self.tpm_visit, 'accept', self.tpm_user)
        self._add_attachment('report', self.tpm_visit)
        self._do_transition(self.tpm_visit, 'send_report', self.tpm_user)
        self._do_transition(self.tpm_visit, 'approve', self.unicef_focal_point)
        self.tpm_visit = self._refresh_tpm_visit_instace(self.tpm_visit)
        self.assertEquals(self.tpm_visit.status, 'unicef_approved')
        self.assertEquals(TPMActivityActionPoint.objects.filter(tpm_activity__tpm_visit=self.tpm_visit).count(), 0)

    def test_action_points(self):
        self._approve_visit()
        self.assertEquals(TPMActivityActionPoint.objects.filter(tpm_activity__tpm_visit=self.tpm_visit).count(), 0)

        response = self.forced_auth_req(
            'patch',
            '/api/tpm/visits/{}/'.format(self.tpm_visit.id),
            user=self.unicef_focal_point,
            data={
                'tpm_activities': [{
                    'id': activity.id,
                    'action_points': [
                        {
                            "section": self.tpm_visit.sections.values_list('id', flat=True)[0],
                            "locations": activity.locations.values_list('id', flat=True),
                            "person_responsible": self.tpm_visit.tpm_partner.staff_members.first().user.id,
                            "cp_outputs": [activity.cp_output.id, ],
                            "due_date": (datetime.now().date() + timedelta(days=5)).strftime('%Y-%m-%d'),
                            "description": "Description",
                        }
                    ]
                } for activity in self.tpm_visit.tpm_activities.all()]
            }
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertNotEquals(TPMActivityActionPoint.objects.filter(tpm_activity__tpm_visit=self.tpm_visit).count(), 0)

    def test_action_point_with_not_related_section(self):
        self._approve_visit()
        self.assertEquals(TPMActivityActionPoint.objects.filter(tpm_activity__tpm_visit=self.tpm_visit).count(), 0)

        response = self.forced_auth_req(
            'patch',
            '/api/tpm/visits/{}/'.format(self.tpm_visit.id),
            user=self.unicef_focal_point,
            data={
                'tpm_activities': [{
                    'id': activity.id,
                    'action_points': [
                        {
                            "section": SectionFactory.create().id,
                            "locations": activity.locations.values_list('id', flat=True),
                            "person_responsible": self.tpm_visit.tpm_partner.staff_members.first().user.id,
                            "cp_outputs": [activity.cp_output.id, ],
                            "due_date": (datetime.now().date() + timedelta(days=5)).strftime('%Y-%m-%d'),
                            "description": "Description",
                        }
                    ]
                } for activity in self.tpm_visit.tpm_activities.all()]
            }
        )
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(TPMActivityActionPoint.objects.filter(tpm_activity__tpm_visit=self.tpm_visit).count(), 0)


class TestTPMFirmViewSet(TPMTestCaseMixin, APITenantTestCase):
    def setUp(self):
        super(TestTPMFirmViewSet, self).setUp()
        self.second_tpm_partner = TPMPartnerFactory()

    def _test_list_view(self, user, expected_firms):
        response = self.forced_auth_req(
            'get',
            '/api/tpm/partners/',
            user=user
        )

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(
            sorted(map(lambda x: x['id'], response.data['results'])),
            sorted(map(lambda x: x.id, expected_firms))
        )

    def test_unicef_list_view(self):
        self._test_list_view(self.unicef_user, [self.tpm_partner, self.second_tpm_partner])

    def test_auditor_list_view(self):
        self._test_list_view(self.tpm_user, [self.tpm_partner])

    def test_usual_user_list_view(self):
        self._test_list_view(self.usual_user, [])


class TestTPMStaffMembersViewSet(TPMTestCaseMixin, APITenantTestCase):
    def test_list_view(self):
        response = self.forced_auth_req(
            'get',
            '/api/tpm/partners/{0}/staff-members/'.format(self.tpm_partner.id),
            user=self.pme_user
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        response = self.forced_auth_req(
            'get',
            '/api/tpm/partners/{0}/staff-members/'.format(self.tpm_partner.id),
            user=self.usual_user
        )
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_view(self):
        response = self.forced_auth_req(
            'get',
            '/api/tpm/partners/{0}/staff-members/{1}/'.format(
                self.tpm_partner.id,
                self.tpm_partner.staff_members.first().id
            ),
            user=self.pme_user
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        response = self.forced_auth_req(
            'get',
            '/api/tpm/partners/{0}/staff-members/{1}/'.format(
                self.tpm_partner.id,
                self.tpm_partner.staff_members.first().id
            ),
            user=self.usual_user
        )
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_view(self):
        response = self.forced_auth_req(
            'post',
            '/api/tpm/partners/{0}/staff-members/'.format(
                self.tpm_partner.id,
                self.tpm_partner.staff_members.first().id
            ),
            data={
                "user": {
                    "email": "test_email_1@gmail.com",
                    "first_name": "John",
                    "last_name": "Doe"
                }
            },
            user=self.pme_user
        )
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        response = self.forced_auth_req(
            'post',
            '/api/tpm/partners/{0}/staff-members/'.format(
                self.tpm_partner.id,
                self.tpm_partner.staff_members.first().id
            ),
            data={
                "user": {
                    "email": "test_email_2@gmail.com",
                    "first_name": "John",
                    "last_name": "Doe"
                }
            },
            user=self.usual_user
        )
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_view(self):
        response = self.forced_auth_req(
            'patch',
            '/api/tpm/partners/{0}/staff-members/{1}/'.format(
                self.tpm_partner.id,
                self.tpm_partner.staff_members.first().id
            ),
            data={
                "user": {
                    "first_name": "John",
                    "last_name": "Doe"
                }
            },
            user=self.pme_user
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        response = self.forced_auth_req(
            'patch',
            '/api/tpm/partners/{0}/staff-members/{1}/'.format(
                self.tpm_partner.id,
                self.tpm_partner.staff_members.first().id
            ),
            data={
                "user": {
                    "first_name": "John",
                    "last_name": "Doe"
                }
            },
            user=self.usual_user
        )
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
