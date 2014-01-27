import decimal
from carshare.models import Driver
# Create your views here.
from django.views.generic import ListView
from operator import itemgetter


def v_dist(v1, v2):
    return sum([(a - b)**2 for a, b in zip(v1, v2)])


def get_closest(my_loc, points):
    dists = [v_dist((p.position.latitude, p.position.longitude), my_loc) for p in points]
    return min(enumerate(dists), key=itemgetter(1))[0]


class Carshare(ListView):
    model = Driver
    context_object_name = 'all_pointers'

    def get_context_data(self, **kwargs):
        my_loc = (decimal.Decimal(self.kwargs['lat']), decimal.Decimal(self.kwargs['long']))
        ctx = super(Carshare, self).get_context_data(**kwargs)
        ctx['closest_idx'] = get_closest(my_loc, Driver.objects.all())
        ctx['my_loc'] = (float(self.kwargs['lat']), float(self.kwargs['long']))  # formatted nicely
        return ctx

