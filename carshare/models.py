# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from django.db.models import DateTimeField, IntegerField
from geoposition.fields import GeopositionField
from django_extensions.db import fields as extensions
from sorl.thumbnail import ImageField


class Driver(models.Model):
    position = GeopositionField()
    owner = models.ForeignKey('auth.User', related_name='drivers', default=1, null=False)


class Passenger(models.Model):
    position = GeopositionField()  # might not be necessary
    owner = models.ForeignKey('auth.User', related_name='passengers', default=1, null=False)


class ActiveRequest(models.Model):
    owner = models.ForeignKey('auth.User')
    position = GeopositionField()
    destination = GeopositionField()
    request_time = DateTimeField(auto_now=True)
    num_passengers = IntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    successful = models.BooleanField(default=False)


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    profile_photo = models.ImageField(upload_to='profiles/')

    def image_tag(self):
        return u'<img src="%s" />' % self.profile_photo.url
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def __str__(self):
        return "%s's profile" % self.user
