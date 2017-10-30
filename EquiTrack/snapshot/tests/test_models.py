from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from EquiTrack.factories import (
    ActivityFactory,
    InterventionFactory,
    UserFactory,
)
from EquiTrack.tests.mixins import FastTenantTestCase as TenantTestCase
from snapshot.models import Activity


class TestActivity(TenantTestCase):
    def test_str(self):
        user = UserFactory()
        intervention = InterventionFactory()
        activity = ActivityFactory(
            target=intervention,
            action=Activity.CREATE,
            by_user=user
        )
        self.assertEqual(
            str(activity),
            "{} {} {}".format(user, Activity.CREATE, intervention)
        )

    def test_by_user_display_empty(self):
        user = UserFactory()
        activity = ActivityFactory(by_user=user)
        self.assertEqual(str(user), "")
        self.assertEqual(activity.by_user_display(), user.email)

    def test_by_user_display(self):
        user = UserFactory(first_name="First")
        activity = ActivityFactory(by_user=user)
        self.assertEqual(str(user), "First")
        self.assertEqual(activity.by_user_display(), "First")
