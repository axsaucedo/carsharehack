from django.db import models
from geoposition.fields import GeopositionField
from django.contrib.auth.models import User
# Create your models here.


class Driver(models.Model):
    name = models.CharField(max_length=200)
    position = GeopositionField()


class MyUser(User):
    """
    Class of the user that can sign up to the service. May be passenger or driver.
    Inherits all from User and has extra such as position.
    User can only be one of driver/passenger, so set is_driver flag.
    """
    position = GeopositionField()
    is_driver = models.BooleanField(default=False)
