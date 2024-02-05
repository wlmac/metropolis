from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
    extend_schema_serializer,
)
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

__all__ = ["staff", "StaffSerializer"]

from core.api.serializers.custom import SingleUserField
from core.models import StaffMember


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "A staff member",
            value={
                "user": 746,
                "bio": "Hi, I'm jason and here is my BIO",
                "positions": ["Doodle Developer"],
                "positions_leading": ["Backend Developer"],
                "years": [
                    "2022-2023",
                    "2023-2024",
                ],
                "is_alumni": False,
            },
        )
    ]
)
class StaffSerializer(serializers.ModelSerializer):
    user = SingleUserField()
    bio = serializers.CharField()
    is_alumni = serializers.BooleanField(read_only=True)

    class Meta:
        model = StaffMember
        fields = ["user", "bio", "positions", "positions_leading", "years", "is_alumni"]


@extend_schema(
    description="Returns a list of all staff.",
    responses={200: StaffSerializer(many=True)},
    parameters=[
        OpenApiParameter(
            "year",
            str,
            OpenApiParameter.QUERY,
            description="the year to filter staff by",
            examples=[
                OpenApiExample(
                    "The year 2023",
                    "2023-2024",
                    description="Only show members who were in metro in 2023-24",
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
        return Response(StaffSerializer(qs.filter(years=[year]), many=True).data)
    return Response(StaffSerializer(qs, many=True).data)
