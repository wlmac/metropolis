from django.utils import timezone
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

__all__ = ["staff"]

from core.api.serializers.custom import SingleUserField
from core.models import StaffMember

class StaffSerializer(serializers.ModelSerializer):
    user = SingleUserField()
    bio = serializers.CharField()
    is_alumni = serializers.ReadOnlyField()
    
    
    class Meta:
        model = StaffMember
        fields = ["user", "bio", "positions", "positions_leading", "years", "is_alumni"]

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
