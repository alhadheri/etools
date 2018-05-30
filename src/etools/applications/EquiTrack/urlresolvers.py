from __future__ import absolute_import, division, print_function, unicode_literals

from django.db import connection
from django.urls import reverse
from django.utils.http import urlquote

from etools.applications.EquiTrack.utils import get_current_site
from etools.applications.users.models import Country


def site_url():
    return 'https://{0}'.format(
        get_current_site().domain
    )


def build_frontend_url(*parts):
    return '{domain}{change_country_view}?country={country_id}&next={next}'.format(
        domain=site_url(),
        change_country_view=reverse('users:country-change'),
        country_id=Country.objects.get(schema_name=connection.schema_name).id,
        next=urlquote('/'.join(map(str, ('',) + parts))),
    )