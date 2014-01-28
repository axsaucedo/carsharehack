from django.conf.urls import patterns, include, url

from django.contrib import admin
from carshare.views import Carshare
from django.views.generic import TemplateView

admin.autodiscover()
re_scientific = r'[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?'
urlpatterns = patterns('',
    # Examples:
    url(r'^carshare/$', TemplateView.as_view(template_name='carshare/base_bounce.html'), name='bounce'),
    url(r'^carshare/long=(?P<long>' + re_scientific + r'),lat=(?P<lat>' + re_scientific + r')$',
        Carshare.as_view(template_name='carshare/base_drivers.html'), name='home'),
    url(r'^admin/', include(admin.site.urls)),
)
