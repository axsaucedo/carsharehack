# Create your models here.
from django.db import models
from geoposition.fields import GeopositionField


class Driver(models.Model):
    position = GeopositionField()
    owner = models.ForeignKey('auth.User', related_name='drivers')


class Passenger(models.Model):
    position = GeopositionField()
    owner = models.ForeignKey('auth.User', related_name='passengers')