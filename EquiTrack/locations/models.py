__author__ = 'jcranwellward'

from django.contrib.gis.db import models


class Governorate(models.Model):
    name = models.CharField(max_length=45L, unique=True)
    area = models.PolygonField(null=True, blank=True)

    objects = models.GeoManager()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Region(models.Model):
    governorate = models.ForeignKey(Governorate)
    name = models.CharField(max_length=45L, unique=True)
    area = models.PolygonField(null=True, blank=True)

    objects = models.GeoManager()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Caza'
        ordering = ['name']


class Locality(models.Model):
    region = models.ForeignKey(Region)
    cad_code = models.CharField(max_length=11L)
    cas_code = models.CharField(max_length=11L)
    cas_code_un = models.CharField(max_length=11L)
    name = models.CharField(max_length=128L)
    cas_village_name = models.CharField(max_length=128L)
    area = models.PolygonField(null=True, blank=True)

    objects = models.GeoManager()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Cadastral/Locality'
        unique_together = ('name', 'cas_code_un')
        ordering = ['name']


class GatewayType(models.Model):
    name = models.CharField(max_length=64L, unique=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Location(models.Model):

    name = models.CharField(max_length=254L)
    locality = models.ForeignKey(Locality)
    gateway = models.ForeignKey(GatewayType, verbose_name='Gateway type')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    p_code = models.CharField(max_length=32L, blank=True, null=True)

    point = models.PointField()
    objects = models.GeoManager()

    def __unicode__(self):
        return u'{} ({} {})'.format(
            self.name,
            self.gateway.name,
            "{}: {}".format(
                'CERD' if self.gateway.name == 'School' else 'P Code',
                self.p_code if self.p_code else ''
            )
        )

    class Meta:
        unique_together = ('name', 'gateway', 'p_code')
        ordering = ['name']
