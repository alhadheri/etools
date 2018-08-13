from django.core.management.base import BaseCommand, CommandError

from etools.applications.EquiTrack.models import Domain
from etools.applications.publics.models import Currency
from etools.applications.users.models import Country


class Command(BaseCommand):
    help = 'Create a new country and related schema'

    def add_arguments(self, parser):
        parser.add_argument('country_name', type=str)

    def handle(self, *args, **options):
        try:
            name = options['country_name']
            usd = Currency.objects.get(code='USD')
            schema_name = name.lower().replace(' ', '_').strip()
            workspace = Country.objects.create(
                schema_name=schema_name,
                name=name,
                local_currency=usd,
            )
            Domain.objects.create(tenant=workspace, domain=f'{schema_name}.etools.unicef.org')
        except Exception as exp:
            raise CommandError(*exp.args)
