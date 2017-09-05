import logging

from django.db import transaction

from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
)

from EquiTrack.validation_mixins import ValidatorViewMixin

from partners.models import (
    Intervention,
)
from partners.serializers.interventions_v2 import (
    InterventionDetailSerializer,
    InterventionCreateUpdateSerializer,
    InterventionBudgetCUSerializer,
    PlannedVisitsCUSerializer,
    InterventionAttachmentSerializer,
    InterventionAmendmentCUSerializer,
    InterventionSectorLocationCUSerializer,
    InterventionResultCUSerializer,
)
from partners.serializers.interventions_v3 import InterventionDetailSerializerV3
from partners.validation.interventions import InterventionValid
from partners.permissions import PartneshipManagerPermission


class InterventionDetailAPIViewV3(ValidatorViewMixin, RetrieveUpdateDestroyAPIView):
    """
    V3 of the Intervention Detail API
    """
    queryset = Intervention.objects.detail_qs().all()
    serializer_class = InterventionDetailSerializerV3
    permission_classes = (PartneshipManagerPermission,)

    SERIALIZER_MAP = {
        'planned_budget': InterventionBudgetCUSerializer,
        'planned_visits': PlannedVisitsCUSerializer,
        'attachments': InterventionAttachmentSerializer,
        'amendments': InterventionAmendmentCUSerializer,
        'sector_locations': InterventionSectorLocationCUSerializer,
        'result_links': InterventionResultCUSerializer
    }

    def get_serializer_class(self):
        """
        Use different serilizers for methods
        """
        if self.request.method in ["PATCH", "PUT"]:
            return InterventionCreateUpdateSerializer
        return super(InterventionDetailAPIViewV3, self).get_serializer_class()

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        related_fields = ['planned_budget', 'planned_visits',
                          'attachments', 'amendments',
                          'sector_locations', 'result_links']
        nested_related_names = ['ll_results']
        instance, old_instance, serializer = self.my_update(
            request,
            related_fields,
            nested_related_names=nested_related_names,
            snapshot=True, **kwargs)

        validator = InterventionValid(instance, old=old_instance, user=request.user)
        if not validator.is_valid:
            logging.debug(validator.errors)
            raise ValidationError(validator.errors)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # refresh the instance from the database.
            instance = self.get_object()

        return Response(InterventionDetailSerializer(instance, context=self.get_serializer_context()).data)


