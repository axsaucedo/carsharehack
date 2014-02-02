from carshare.models import Driver, Passenger
from django.contrib import admin


class DriverAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'position')


class PassengerAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'position')

admin.site.register(Driver, DriverAdmin)
admin.site.register(Passenger, PassengerAdmin)