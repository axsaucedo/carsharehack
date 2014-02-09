import decimal
import json
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.decorators.http import require_POST
from rest_framework.reverse import reverse
from carshare.models import Driver, Passenger, ActiveRequest
from carshare.permissions import IsOwnerOrReadOnly, IsOwner, PassengerPermissions,  \
    DriverCheckInPermissions, PassengerAddRequestPermissions
from carshare.serializers import UserSerializer, DriverSerializer, PassengerSerializer, GeopositionFieldSerializer, \
    ValidRequestSerializer
from geoposition import Geoposition
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


@login_required(login_url='/login/')
def passengerRequest(request):

    active = ActiveRequest.objects.filter(owner=request.user, active=True)

    if request.method == "POST":
        try:
            if active:
                return render(request, 'carshare/passenger.html', { 'active' : active })

            else:
                post = request.POST

                currlat = post['currlat']
                currlong = post['currlong']
                destlat = post['destlat']
                destlong = post['destlong']
                price = post['price']
                passengers = post['passengers']
                owner = request.user

                ar = ActiveRequest(   owner=owner
                                    , position=Geoposition(currlat, currlong)
                                    , destination=Geoposition(destlat, destlong)
                                    , price=price
                                    , num_passengers=passengers)

                ar.save()

                active = True

        except:
            pass

    return render(request, 'carshare/passenger.html', { 'active' : active })

def viewProfile(request, username):

    user = User.objects.get(username=username)

    return render(request, 'accounts/profile.html', { 'user' : user })

class DriverCheckinViewSet(viewsets.ModelViewSet):
    """
    Whenever a driver checks in, they also create a view with any valid travel requests.
    """
    model = ActiveRequest
    serializer_class = ValidRequestSerializer
    permission_classes = [permissions.IsAuthenticated, DriverCheckInPermissions]
    paginate_by = 10

    def get_queryset(self):
        """
        Queryset is the requests located near them.
        """
        lat = self.request.GET.get("latitude", "")
        long = self.request.GET.get("longitude", "")

        qs = ActiveRequest.objects.filter(inprogress=False).filter(active=True).filter(successful=False)
        current_driver = Driver.objects.get(owner__id=self.request.user.id)
        current_driver.position = Geoposition(lat, long)
        current_driver.save()

        dist_lam = lambda x: get_closest(x, current_driver)
        ordered_requests = sorted(qs, key=dist_lam)

        return ordered_requests

class PassengerAddRequestViewSet(viewsets.ModelViewSet):
    model = ActiveRequest
    serializer_class = ValidRequestSerializer
    permission_classes = [permissions.IsAuthenticated, PassengerAddRequestPermissions]

    def get_queryset(self):
        return ActiveRequest.objects.filter(owner__id=self.request.user.id)


def passenger_post_request(request):
    #return HttpResponse(json.dumps(response_data), content_type="application/json")
    return HttpResponseRedirect(reverse('activerequest-list') + '?format=json')


def logout_view(request):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect('/')


import json
@require_POST
def driver_accept_request(request):
    """
    The driver has accepted an active request.
    Find active request and set it to in progress
    """
    response = {}

    try:
        activerequestid = request.POST['activerequestid']  # a dict of json stuff
        this_request = ActiveRequest.objects.get(id=int(activerequestid))
        this_request.inprogress = True
        this_request.save()

    except e:
        print e
        response = { "error" :  e }

    return HttpResponse(json.dumps(response), content_type="application/json")





# @require_POST
# def passenger_accept_driver(request):
#     """
#     The passenger has accepted a driver.
#     Find active request and set it to successful
#     """
#     if request.method == 'POST':
#         data = json.loads(request.raw_post_data)  # a dict of json stuff
#         active_request_id = data['activerequestid']
#         this_request = ActiveRequest.objects.get(id=active_request_id)
#         this_request.successful = True
#         this_request.inprogress = False
#         this_request.save()

