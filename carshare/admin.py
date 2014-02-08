from carshare.models import Driver, Passenger, UserProfile, ActiveRequests
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class DriverAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'position')


class PassengerAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'position')

admin.site.unregister(User)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    #list_display = ('username', 'email', 'profile_image',)
    readonly_fields = ('image_tag',)


class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline]
    list_display = ('username', 'first_name', 'last_name', 'email',)



admin.site.register(User, UserProfileAdmin)

admin.site.register(Driver, DriverAdmin)
admin.site.register(Passenger, PassengerAdmin)
admin.site.register(ActiveRequests)