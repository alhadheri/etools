from django.contrib import admin

from etools.applications.EquiTrack.models import Domain


class DomainAdmin(admin.ModelAdmin):
    fields = ['domain', 'tenant']


admin.site.register(Domain, DomainAdmin)
