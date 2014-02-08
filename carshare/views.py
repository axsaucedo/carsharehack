import decimal
from carshare.models import Driver, Passenger, ActiveRequest
from carshare.permissions import IsOwnerOrReadOnly, IsOwner, PassengerPermissions, DriverPermissions
from carshare.serializers import UserSerializer, DriverSerializer, PassengerSerializer, GeopositionFieldSerializer, \
    ValidRequestSerializer
from django.contrib.auth.models import User
from django.views.generic import ListView, TemplateView
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAdminUser
from rest_framework import mixins


def v_dist(v1, v2):
    return sum([(a - b)**2 for a, b in zip(v1, v2)])


def get_closest(p1, p2):
    v1 = (decimal.Decimal(p1.position.latitude), decimal.Decimal(p1.position.longitude))
    v2 = (decimal.Decimal(p2.position.latitude), decimal.Decimal(p2.position.longitude))
    return v_dist(v1, v2)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]  # only admin can see


class PassengerViewSet(viewsets.ModelViewSet):
    model = Passenger
    serializer_class = PassengerSerializer
    permission_classes = [permissions.IsAuthenticated, PassengerPermissions]

    # def pre_save(self, obj):
    #     obj.owner = self.request.user
    def get_queryset(self):
        return Passenger.objects.filter(owner__id=self.request.user.id)


# class UpdatePositionViewSet(viewsets.ViewSet):
#     model = Passenger
#     serializer_class = GeopositionFieldSerializer
#     permission_classes = [permissions.IsAuthenticated, PassengerPermissions]
#
#     def get_queryset(self):
#         return Passenger.objects.filter(owner__id=self.request.user.id)


# class DriverViewSet(viewsets.ReadOnlyModelViewSet):
#     """
#     Lists the closest drivers to the currently logged in user ordered by distance.
#     """
#     model = Driver
#     serializer_class = DriverSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     paginate_by = 10
#
#     def pre_save(self, obj):  # necessary?
#         obj.owner = self.request.user
#
#     def get_queryset(self):
#         qs = Driver.objects.exclude(owner__id=self.request.user.id)
#         try:
#             current_passenger = Passenger.objects.get(owner__id=self.request.user.id)  # find the passenger
#         except Passenger.DoesNotExist:
#             raise PermissionDenied  # Raises error in API
#         dist_lam = lambda x: get_closest(x, current_passenger)
#         ordered_drivers = sorted(qs, key=dist_lam)
#         return ordered_drivers


class DriverCheckinViewSet(viewsets.ModelViewSet):
    """
    Whenever a driver checks in, they also create a view with any valid travel requests.
    """
    model = ActiveRequest
    serializer_class = ValidRequestSerializer
    permission_classes = [permissions.IsAuthenticated, DriverPermissions]
    paginate_by = 10

    def get_queryset(self):
        """
        Queryset is the requests located near them.
        """
        qs = ActiveRequest.objects.all()
        current_driver = Driver.objects.get(owner__id=self.request.user.id)
        dist_lam = lambda x: get_closest(x, current_driver)
        ordered_requests = sorted(qs, key=dist_lam)
        return ordered_requests

