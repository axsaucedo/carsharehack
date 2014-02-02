import decimal
from carshare.models import Driver, Passenger
from django.contrib.auth.models import User
from geoposition import Geoposition
from rest_framework import serializers
__author__ = 'srd1g10'


class GeopositionFieldSerializer(serializers.WritableField):
    def from_native(self, data):
        data = data.strip('(').rstrip(')')
        latitude, longitude = [decimal.Decimal(col) for col in data.split(',')]
        return Geoposition(latitude, longitude)

    def to_native(self, obj):
        return "({}, {})".format(obj.latitude, obj.longitude)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'first_name', 'last_name', 'email')


class DriverSerializer(serializers.HyperlinkedModelSerializer):
    position = GeopositionFieldSerializer(source="position", write_only=True)
    owner = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True)

    class Meta:
        model = Driver
        fields = ('url', 'owner', 'position')


class PassengerSerializer(serializers.HyperlinkedModelSerializer):
    position = GeopositionFieldSerializer(source="position", write_only=True)
    owner = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True)

    class Meta:
        model = Passenger
        fields = ('url', 'owner', 'position')