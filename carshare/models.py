from django.db import models
from geoposition.fields import GeopositionField
# Create your models here.


class Driver(models.Model):
    name = models.CharField(max_length=200)
    position = GeopositionField()
