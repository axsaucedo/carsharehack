#from accounts.models import UserProfile
#from accounts.models import Driver
from carshare.models import Driver, Passenger
from django.contrib import admin
# Register your models here.
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


# class UserInline(admin.StackedInline):
#     model = UserProfile
#     can_delete = False
#     verbose_name_plural = 'user'
#
#
# class UserAdmin(UserAdmin):
#     inlines = (UserInline, )
#
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
admin.site.register(Driver)
admin.site.register(Passenger)