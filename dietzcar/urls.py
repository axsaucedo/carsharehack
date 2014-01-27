from django.conf.urls import patterns, include, url

from django.contrib import admin
from carshare.views import Carshare
from django.views.generic import TemplateView

admin.autodiscover()
re_scientific = "[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?"
urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'carshare.views.index', name='home'),
    url(r'^$', TemplateView.as_view(template_name='carshare/base_bounce.html'), name='bounce'),
    url(r'^long=(?P<long>[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?),lat=(?P<lat>[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)',
        Carshare.as_view(template_name='carshare/base_drivers.html'), name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^$', 'dietzcar.views.index'),
    url(r'^admin/', include(admin.site.urls)),
)
