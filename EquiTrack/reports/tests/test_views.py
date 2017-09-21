import datetime

from django.core.urlresolvers import reverse
from rest_framework import status

from reports.models import ResultType, CountryProgramme, Disaggregation
from EquiTrack.factories import (
    UserFactory,
    ResultFactory,
    CountryProgrammeFactory,
    DisaggregationFactory,
)
from EquiTrack.tests.mixins import APITenantTestCase


class TestReportViews(APITenantTestCase):
    fixtures = ['initial_data.json']

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(is_staff=True)  # UNICEF staff user
        cls.result_type = ResultType.objects.get(name=ResultType.OUTPUT)

        today = datetime.date.today()
        cls.country_programme = CountryProgrammeFactory(
            wbs='0000/A0/01',
            from_date=datetime.date(today.year - 1, 1, 1),
            to_date=datetime.date(today.year + 1, 1, 1))

        cls.result1 = ResultFactory(
            result_type=cls.result_type,
            country_programme=cls.country_programme,
        )

        cls.result2 = ResultFactory(
            result_type=cls.result_type,
            country_programme=cls.country_programme
        )
        cls.v2_results_url = reverse('report-result-list')

    def test_api_resulttypes_list(self):
        url = reverse('resulttypes-list')
        response = self.forced_auth_req('get', url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_sectors_list(self):
        url = reverse('sectors-list')
        response = self.forced_auth_req('get', url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_indicators_list(self):
        url = reverse('indicators-list')
        response = self.forced_auth_req('get', url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_results_list(self):
        url = reverse('results-list')
        response = self.forced_auth_req('get', url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(int(response.data[0]["id"]), self.result1.id)

    def test_api_results_patch(self):
        url = reverse('results-detail', args=[self.result1.id])
        data = {"name": "patched name"}
        response = self.forced_auth_req('patch', url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "patched name")

    def test_api_units_list(self):
        url = reverse('units-list')
        response = self.forced_auth_req('get', url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # V2 URLs

    def test_apiv2_results_list(self):
        response = self.forced_auth_req('get', self.v2_results_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(int(response.data[0]["id"]), self.result1.id)

    def test_apiv2_results_list_minimal(self):
        data = {"verbosity": "minimal"}
        response = self.forced_auth_req('get', self.v2_results_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0].keys(), ["id", "name"])

    def test_apiv2_results_retrieve(self):
        detail_url = reverse('report-result-detail', args=[self.result1.id])
        response = self.forced_auth_req('get', detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(int(response.data["id"]), self.result1.id)

    def test_apiv2_results_list_current_cp(self):
        response = self.forced_auth_req('get', self.v2_results_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(int(response.data[0]["country_programme"]), CountryProgramme.objects.all_active.first().id)

    def test_apiv2_results_list_filter_year(self):
        data = {"year": datetime.date.today().year}
        response = self.forced_auth_req('get', self.v2_results_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_apiv2_results_list_filter_cp(self):
        data = {"country_programme": self.result1.country_programme.id}
        response = self.forced_auth_req('get', self.v2_results_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(int(response.data[0]["id"]), self.result1.id)

    def test_apiv2_results_list_filter_result_type(self):
        data = {"result_type": self.result_type.name}
        response = self.forced_auth_req('get', self.v2_results_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(int(response.data[0]["id"]), self.result1.id)

    def test_apiv2_results_list_filter_values(self):
        data = {"values": '{},{}'.format(self.result1.id, self.result2.id)}
        response = self.forced_auth_req('get', self.v2_results_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_apiv2_results_list_filter_values_bad(self):
        data = {"values": '{},{}'.format('23fg', 'aasd67')}
        response = self.forced_auth_req('get', self.v2_results_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, ['ID values must be integers'])

    def test_apiv2_results_list_filter_combined(self):
        data = {
            "result_type": self.result_type.name,
            "year": datetime.date.today().year,
        }
        response = self.forced_auth_req('get', self.v2_results_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.result1.id, [int(i["id"]) for i in response.data])


class TestDisaggregationViews(APITenantTestCase):
    """
    Very minimal testing, just to make sure things work.
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(is_staff=True)
        cls.url = reverse('disaggregation-list-create')

    def test_get(self):
        """
        GET returns a list of Disaggregations.
        """
        num_instances = 3
        DisaggregationFactory.create_batch(size=num_instances)
        response = self.forced_auth_req('get', self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), num_instances)

    def test_post(self):
        """
        POST creates a Disaggregation, with DisaggregationValues.
        """
        data = {
            'name': 'Gender',
            'disaggregation_values': [
                {'value': 'Female'},
                {'value': 'Male'},
                {'value': 'Other'},
            ]
        }
        response = self.forced_auth_req('post', self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        disaggregation = Disaggregation.objects.get()
        self.assertEqual(disaggregation.name, 'Gender')
        self.assertEqual(disaggregation.disaggregation_values.count(), 3)
