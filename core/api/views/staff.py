from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

__all__ = ["staff", "StaffSerializer"]

from core.api.serializers.custom import SingleUserField
from core.models import StaffMember


class StaffSerializer(serializers.ModelSerializer):
    user = SingleUserField()
    bio = serializers.CharField()
    is_alumni = serializers.ReadOnlyField()

    class Meta:
        model = StaffMember
        fields = ["user", "bio", "positions", "positions_leading", "years", "is_alumni"]


@extend_schema(
    description="Returns a list of all staff.",
    responses={200: StaffSerializer(many=True)},
    parameters=[
        OpenApiParameter(
            "year",
            int,
            OpenApiParameter.QUERY,
            description="the year to filter staff by",
            examples=[
                OpenApiExample(
                    "The year 2023",
                    2023,
                    description="Only show members who were in metro in 2024",
                ),
            ],
        ),
    ],
)
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
    # todo test below
    qs = StaffMember.objects.filter(is_active=True)
    if request.GET.get("year"):
        year = request.GET.get("year")
        return Response(
            StaffSerializer(
                qs.filter(years__contains=[year]), many=True
            ).data
        )
    return Response(StaffSerializer(qs, many=True).data)
