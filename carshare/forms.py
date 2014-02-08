from django.contrib.auth.models import User
from django.forms import ModelForm
from carshare.models import ActiveRequest

__author__ = 'srd1g10'


class PassengerRequestForm(ModelForm):
    class Meta:
        model = ActiveRequest
        fields = ('position', 'destination', 'request_time', 'num_passengers')