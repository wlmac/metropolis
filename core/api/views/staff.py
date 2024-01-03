from collections import defaultdict
from typing import Literal

from django.conf import settings
from django.utils import timezone
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

__all__ = ["staff"]

from core.api.serializers.custom import SingleUserField
from core.models import StaffMember

staff_roles = defaultdict(list)
for role, users in settings.METROPOLIS_STAFFS.items():
    for user in users:
        staff_roles[user].append(role)


class StaffSerializer(serializers.ModelSerializer):
    user = SingleUserField()
    bio = serializers.CharField()
    
    class Meta:
        model = StaffMember
        fields = ["user", "bio", "positions", "years"]

@api_view(["GET"])
def staff(request, year=None):
    """
    Returns a list of all staff.
    Args:
        year: The year to get staff for. If not specified, returns staff from the current year.
        the format for the year is "2023-24".
    Returns:
        A list of all staff.
    """
    if year is None:
        year = f"{timezone.now().year}-{str(timezone.now().year + 1)[-2:]}"
    # todo add filtering via year
    return Response(StaffSerializer(StaffMember.objects.all(), many=True).data)
