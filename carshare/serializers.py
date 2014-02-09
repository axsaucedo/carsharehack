import decimal
from carshare.models import Driver, Passenger, ActiveRequest
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
    position = GeopositionFieldSerializer(source="position")
    #owner = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True)
    username = serializers.RelatedField(source='owner.username', read_only=True)
    email = serializers.RelatedField(source='owner.email')
    first_name = serializers.RelatedField(source='owner.first_name')
    last_name = serializers.RelatedField(source='owner.last_name')

    class Meta:
        model = Driver
        fields = ('position', 'username', 'email', 'first_name', 'last_name')


class PassengerSerializer(serializers.HyperlinkedModelSerializer):
    position = GeopositionFieldSerializer(source="position", )
    #owner = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True)

    class Meta:
        model = Passenger
        fields = ('position', )


class ValidRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveRequest
        fields = ('id', 'position', 'destination', 'request_time', 'num_passengers', 'price', 'owner')


# class DriverCheckInSerializer(serializers.HyperlinkedModelSerializer):
#     #valid_requests = ValidRequestSerializer(source='valid_requests')
#
#     class Meta:
#         model = ActiveRequest
#         fields = ('valid_requests', )
