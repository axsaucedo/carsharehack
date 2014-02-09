from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework.reverse import reverse, reverse_lazy
from carshare.views import PassengerViewSet, DriverCheckinViewSet, PassengerAddRequestViewSet
#from django.contrib.auth.decorators import login_required
#from carshare.views import DriverViewSet, UserViewSet
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static

admin.autodiscover()
re_scientific = r'[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?'
urlpatterns = patterns('',
    # url(r'^$',
    #     login_required(ProfileView.as_view(template_name='dietzcar/index.html')), name='profile'),
    #url(r'^carshare/$', login_required(NearestDriversViewSet.as_view(template_name='carshare/drivers.html')), name='carshare'),
    url(r'^admin/?', include(admin.site.urls)),
    )

router = DefaultRouter()
#router.register(r'drivers', DriverViewSet)
router.register(r'passengers', PassengerViewSet)
router.register(r'drivers', DriverCheckinViewSet)
router.register(r'addrequest', PassengerAddRequestViewSet)
#router.register(r'users', UserViewSet)

urlpatterns += patterns('',
    url(r'^api/', include(router.urls)),
    #url(r'^api/', )
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #url(r'api/passengers/(?P<pk>)', UpdatePassengerPositionDetailView.as_view(), name='passenger-detail'),
)

urlpatterns += patterns('',
                        url(r'^passenger/', TemplateView.as_view(template_name='carshare/passenger.html')),
                        url(r'^driver/', TemplateView.as_view(template_name='carshare/driver.html')),
                        url(r'accounts/', include('social.apps.django_app.urls', namespace='social')),
                        url(r'^fb/', TemplateView.as_view(template_name='accounts/login.html'), name='login'),
                        url(r'^accounts/profile/', TemplateView.as_view(template_name='carshare/passenger.html')),
                        url(r'^logout/', 'carshare.views.logout_view', name='logout'),
                        url(r'^logout-complete/', TemplateView.as_view(template_name='accounts/logout_complete.html'), name='logout-complete'),
                        url(r'^driver_view_requests/', 'carshare.views.driver_view_requests', name='driver-view-requests'),
                        )
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)