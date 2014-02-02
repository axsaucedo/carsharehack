import decimal
from carshare.models import Driver, Passenger
from carshare.permissions import IsOwnerOrReadOnly, IsOwner, PassengerPermissions, DriverPermissions
from carshare.serializers import UserSerializer, DriverSerializer, PassengerSerializer
from django.contrib.auth.models import User
from django.views.generic import ListView, TemplateView
from operator import itemgetter
from django.views.generic.detail import DetailView
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import IsAdminUser


def v_dist(v1, v2):
    return sum([(a - b)**2 for a, b in zip(v1, v2)])


def get_closest(my_loc, points):
    dists = [v_dist((p[0], p[1]), my_loc) for p in points]
    return min(enumerate(dists), key=itemgetter(1))[0]


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]  # only admin can see


class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [permissions.IsAuthenticated, DriverPermissions]

    def pre_save(self, obj):
        obj.owner = self.request.user


class PassengerViewSet(viewsets.ModelViewSet):
    model = Passenger
    serializer_class = PassengerSerializer
    permission_classes = [permissions.IsAuthenticated, PassengerPermissions]

    def pre_save(self, obj):
        obj.owner = self.request.user

    def get_queryset(self):
        return Passenger.objects.filter(owner__id=self.request.user.id)


class NearestDriversViewSet(ListView):
    model = Driver
    context_object_name = 'drivers'
    paginate_by = 10

    def get_queryset(self):
        return Driver.objects.exclude(owner__id=self.request.user.id)

    def get_context_data(self, **kwargs):
        current_passenger = Passenger.objects.get(owner__id=self.request.user.id)  # find the passenger
        ctx = super(NearestDriversViewSet, self).get_context_data(**kwargs)
        pos = current_passenger.position
        my_loc = (decimal.Decimal(pos.latitude), decimal.Decimal(pos.longitude))
        points = [(decimal.Decimal(d.position.latitude),
                   decimal.Decimal(d.position.longitude)) for d in self.object_list]
        ctx['closest_idx'] = get_closest(my_loc, points)
        ctx['my_loc'] = (float(pos.latitude), float(pos.longitude))  # formatted nicely
        return ctx
