from itertools import chain

from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import connection

from etools.applications.users.models import Country


def get_all_field_names(TheModel):
    '''Return a list of all field names that are possible for this model (including reverse relation names).
    Any internal-only field names are not included.

    Replacement for MyModel._meta.get_all_field_names() which does not exist under Django 1.10.
    https://github.com/django/django/blob/stable/1.7.x/django/db/models/options.py#L422
    https://docs.djangoproject.com/en/1.10/ref/models/meta/#migrating-from-the-old-api
    '''
    return list(set(chain.from_iterable(
        (field.name, field.attname) if hasattr(field, 'attname') else (field.name,)
        for field in TheModel._meta.get_fields()
        if not (field.many_to_one and field.related_model is None) and
        not isinstance(field, GenericForeignKey)
    )))


def run_on_all_tenants(function, **kwargs):
    with every_country() as c:
        for country in c:
            function(**kwargs)


class every_country:
    """
    Loop through every available available tenant/country, then revert back to whatever was set before.

    Example usage:

    with every_country() as c:
        for country in c:
            print(country.name)
            function()
    """
    original_country = None

    def __enter__(self):
        self.original_country = connection.tenant
        for c in Country.objects.exclude(name='Global').all():
            connection.set_tenant(c)
            yield c

    def __exit__(self, type, value, traceback):
        connection.set_tenant(self.original_country)


def strip_text(text):
    return '\r\n'.join(map(lambda line: line.lstrip(), text.splitlines()))


def to_choices_list(value):
    if isinstance(value, dict):
        return value.items()

    return value
