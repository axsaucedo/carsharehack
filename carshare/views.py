import decimal
from carshare.models import Driver, Passenger
from carshare.permissions import IsOwnerOrReadOnly
from carshare.serializers import UserSerializer, DriverSerializer
from django.contrib.auth.models import User
from django.views.generic import ListView, TemplateView
from operator import itemgetter
from rest_framework import permissions
from rest_framework import viewsets


def v_dist(v1, v2):
    return sum([(a - b)**2 for a, b in zip(v1, v2)])


def get_closest(my_loc, points):
    dists = [v_dist((p[0], p[1]), my_loc) for p in points]
    return min(enumerate(dists), key=itemgetter(1))[0]


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def pre_save(self, obj):
        obj.owner = self.request.user


class NearestDriversViewSet(ListView):
    model = Driver
    context_object_name = 'drivers'

    def get_queryset(self):
        return Driver.objects.exclude(owner__id=self.request.user.id)

    def get_context_data(self, **kwargs):
        pos = Passenger.objects.get(owner__id=self.request.user.id).position  # find the passenger
        my_loc = (decimal.Decimal(pos.latitude), decimal.Decimal(pos.longitude))
        ctx = super(NearestDriversViewSet, self).get_context_data(**kwargs)
        points = [(decimal.Decimal(d.position.latitude),
                   decimal.Decimal(d.position.longitude)) for d in self.object_list]
        ctx['closest_idx'] = get_closest(my_loc, points)
        ctx['my_loc'] = (float(pos.latitude), float(pos.longitude))  # formatted nicely
        return ctx


class ProfileView(TemplateView):
    # TODO: add check to see if pk was defined then show that user instead of self
    model = User
    context_object_name = 'user'

