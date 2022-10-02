from collections import defaultdict

from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

__ALL__ = ['staff']


staff_roles = defaultdict(list)
for role, users in settings.METROPOLIS_STAFFS.items():
    for user in users:
        staff_roles[user].append(role)


@api_view()
def staff(request):
    """
    Returns a list of all staff.

    https://noi.nyiyui.ca/k/1063/5041#Get Staff
    """
    return Response([
        dict(user=user, bio=bio, roles=staff_roles[user])
        for user, bio in settings.METROPOLIS_STAFF_BIO.items()
    ])
