from django.contrib.auth.decorators import login_required
from django.core.serializers import json
from django.http import HttpResponse
from django.views.decorators.http import require_POST

__author__ = 'srd1g10'

# @login_required
# @require_POST
# def remove_staff(request):
#     response = {}
#
#     try:
#         staff_id = request.POST["staff_id"]
#
#         staff = Staff.objects.get(id=staff_id)
#         staff.delete()
#
#     except Exception, err:
#         response['error'] = err.__str__()
#
#     return HttpResponse(json.dumps(response), content_type="application/json")