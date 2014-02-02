# Create your models here.
from django.db import models
from geoposition.fields import GeopositionField
from django_extensions.db import fields as extensions


class Driver(models.Model):
    position = GeopositionField()
    owner = models.ForeignKey('auth.User', related_name='drivers', default=1, null=False)


class Passenger(models.Model):
    position = GeopositionField()
    owner = models.ForeignKey('auth.User', related_name='passengers', default=1, null=False)
