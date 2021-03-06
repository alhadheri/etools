from django.core.management.base import BaseCommand, CommandError


from etools.applications.publics.models import Currency
from etools.applications.users.models import Country


class Command(BaseCommand):
    help = 'Create a new country and related schema'

    def add_arguments(self, parser):
        parser.add_argument('country_name', type=str)

    def handle(self, *args, **options):
        try:
            name = options['country_name']
            slug = name.lower().replace(' ', '-').strip()
            usd = Currency.objects.get(code='USD')
            Country.objects.create(
                domain_url='{}.etools.unicef.org'.format(slug),
                schema_name=name.lower().replace(' ', '_').strip(),
                name=name,
                local_currency=usd,
            )
        except Exception as exp:
            raise CommandError(*exp.args)
