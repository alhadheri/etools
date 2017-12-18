from __future__ import unicode_literals

from datetime import timedelta

import factory
from django.utils import timezone
from factory import fuzzy

from locations.tests.factories import LocationFactory
from partners.tests.factories import InterventionFactory
from publics.tests.factories import (
    AirlineCompanyFactory, CurrencyFactory, DSARegionFactory, ExpenseTypeFactory, FundFactory, GrantFactory, WBSFactory
)
from reports.tests.factories import ResultFactory, SectorFactory
from t2f import models
from t2f.models import (
    make_action_point_number,
    make_travel_reference_number,
)
from users.tests.factories import OfficeFactory, UserFactory

_FUZZY_START_DATE = timezone.now() - timedelta(days=5)
_FUZZY_END_DATE = timezone.now() + timedelta(days=5)


class FuzzyTravelType(factory.fuzzy.BaseFuzzyAttribute):
    def fuzz(self):
        return factory.fuzzy._random.choice(
            [t[0] for t in models.TravelType.CHOICES]
        )


class TravelActivityFactory(factory.django.DjangoModelFactory):
    travel_type = models.TravelType.PROGRAMME_MONITORING
    partner = factory.SelfAttribute('partnership.agreement.partner')
    partnership = factory.SubFactory(InterventionFactory)
    result = factory.SubFactory(ResultFactory)
    primary_traveler = factory.SubFactory(UserFactory)
    date = factory.LazyAttribute(lambda o: timezone.now())

    class Meta:
        model = models.TravelActivity

    @factory.post_generation
    def populate_locations(self, create, extracted, **kwargs):
        location = LocationFactory()
        self.locations.add(location)

    @factory.post_generation
    def travels(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for travel in extracted:
                self.travels.add(travel)


class ItineraryItemFactory(factory.DjangoModelFactory):
    origin = fuzzy.FuzzyText(length=32)
    destination = fuzzy.FuzzyText(length=32)
    departure_date = fuzzy.FuzzyDateTime(start_dt=_FUZZY_START_DATE, end_dt=timezone.now())
    arrival_date = fuzzy.FuzzyDateTime(start_dt=timezone.now(), end_dt=_FUZZY_END_DATE)
    dsa_region = factory.SubFactory(DSARegionFactory)
    overnight_travel = False
    mode_of_travel = models.ModeOfTravel.BOAT

    @factory.post_generation
    def populate_airlines(self, create, extracted, **kwargs):
        airline = AirlineCompanyFactory()
        self.airlines.add(airline)

    class Meta:
        model = models.ItineraryItem


class ExpenseFactory(factory.DjangoModelFactory):
    currency = factory.SubFactory(CurrencyFactory)
    amount = fuzzy.FuzzyDecimal(1, 10000)
    type = factory.SubFactory(ExpenseTypeFactory)

    class Meta:
        model = models.Expense


class DeductionFactory(factory.DjangoModelFactory):
    date = fuzzy.FuzzyDateTime(start_dt=_FUZZY_START_DATE, end_dt=_FUZZY_END_DATE)
    breakfast = False
    lunch = False
    dinner = False
    accomodation = False
    no_dsa = False

    class Meta:
        model = models.Deduction


class CostAssignmentFactory(factory.DjangoModelFactory):
    wbs = factory.SubFactory(WBSFactory)
    share = fuzzy.FuzzyInteger(1, 100)
    grant = factory.SubFactory(GrantFactory)
    fund = factory.SubFactory(FundFactory)

    class Meta:
        model = models.CostAssignment


class ClearanceFactory(factory.DjangoModelFactory):
    medical_clearance = True
    security_clearance = True
    security_course = True

    class Meta:
        model = models.Clearances


class ActionPointFactory(factory.DjangoModelFactory):
    action_point_number = factory.Sequence(lambda n: make_action_point_number())
    description = fuzzy.FuzzyText(length=128)
    due_date = fuzzy.FuzzyDateTime(start_dt=_FUZZY_START_DATE, end_dt=timezone.now())
    person_responsible = factory.SubFactory(UserFactory)
    assigned_by = factory.SubFactory(UserFactory)
    status = 'open'
    created_at = timezone.now()

    class Meta:
        model = models.ActionPoint


class TravelFactory(factory.DjangoModelFactory):
    traveler = factory.SubFactory(UserFactory)
    supervisor = factory.SubFactory(UserFactory)
    office = factory.SubFactory(OfficeFactory)
    sector = factory.SubFactory(SectorFactory)
    start_date = fuzzy.FuzzyDateTime(start_dt=_FUZZY_START_DATE, end_dt=timezone.now())
    end_date = fuzzy.FuzzyDateTime(start_dt=timezone.now(), end_dt=_FUZZY_END_DATE)
    purpose = factory.Sequence(lambda n: 'Purpose #{}'.format(n))
    international_travel = False
    ta_required = True
    reference_number = factory.Sequence(lambda n: make_travel_reference_number())
    currency = factory.SubFactory(CurrencyFactory)
    mode_of_travel = []

    itinerary = factory.RelatedFactory(ItineraryItemFactory, 'travel')
    expenses = factory.RelatedFactory(ExpenseFactory, 'travel')
    deductions = factory.RelatedFactory(DeductionFactory, 'travel')
    cost_assignments = factory.RelatedFactory(CostAssignmentFactory, 'travel')
    clearances = factory.RelatedFactory(ClearanceFactory, 'travel')
    action_points = factory.RelatedFactory(ActionPointFactory, 'travel')

    @factory.post_generation
    def populate_activities(self, create, extracted, **kwargs):
        ta = TravelActivityFactory(primary_traveler=self.traveler)
        ta.travels.add(self)

    class Meta:
        model = models.Travel


class InvoiceFactory(factory.DjangoModelFactory):
    travel = factory.SubFactory(TravelFactory)
    business_area = fuzzy.FuzzyText(length=12)
    vendor_number = fuzzy.FuzzyText(length=12)
    currency = factory.SubFactory(CurrencyFactory)
    amount = fuzzy.FuzzyDecimal(0, 1000)
    status = models.Invoice.PENDING
    messages = []

    class Meta:
        model = models.Invoice


class InvoiceItemFactory(factory.DjangoModelFactory):
    invoice = factory.SubFactory(InvoiceFactory)
    wbs = factory.SubFactory(WBSFactory)
    grant = factory.SubFactory(GrantFactory)
    fund = factory.SubFactory(FundFactory)
    amount = fuzzy.FuzzyDecimal(0, 250)

    class Meta:
        model = models.InvoiceItem


class FuzzyTravelStatus(factory.fuzzy.BaseFuzzyAttribute):
    def fuzz(self):
        return factory.fuzzy._random.choice(
            [t[0] for t in models.Travel.CHOICES]
        )
