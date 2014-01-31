from django.conf.urls import patterns, include, url
from django.contrib import admin
from carshare.views import NearestDriversViewSet, ProfileView
from django.contrib.auth.decorators import login_required
from rest_framework.urlpatterns import format_suffix_patterns
from carshare.views import DriverViewSet, UserViewSet
from rest_framework import renderers
from rest_framework.routers import DefaultRouter


admin.autodiscover()
re_scientific = r'[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?'
urlpatterns = patterns('',
    url(r'^$',
        login_required(ProfileView.as_view(template_name='dietzcar/index.html')), name='profile'),
    url(r'^carshare/$', login_required(NearestDriversViewSet.as_view(template_name='carshare/drivers.html')), name='carshare'),
    url(r'^admin/', include(admin.site.urls)),
    )

router = DefaultRouter()
router.register(r'drivers', DriverViewSet)
router.register(r'users', UserViewSet)

urlpatterns += patterns('',
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)