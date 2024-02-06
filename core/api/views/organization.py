from django.db.models import Count
from rest_framework import generics

from .. import serializers
from ..utils import ListAPIViewWithFallback
from ... import models

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework.decorators import api_view
from core.api.serializers.organization import OrganizationSerializer

@extend_schema(
    responses={200: OrganizationSerializer(many=True)},
    parameters=[
        OpenApiParameter(
            "limit",
            int,
            OpenApiParameter.QUERY,
            description="Number of results to return per page.",
        ),
        OpenApiParameter(
            "offset",
            int,
            OpenApiParameter.QUERY,
            description="The initial index from which to return the results.",
        ),
    ],
)
@api_view(["GET"])
def apiOrganizationList(request, year=None):
    queryset = (
        models.Organization.objects.filter(is_active=True)
        .annotate(num_members=Count("member"))
        .order_by("-num_members")
    )
    serializer_class = serializers.OrganizationSerializer

@extend_schema(
    responses={200: OrganizationSerializer(many=True)},
)
@api_view(["GET"])
def organizationDetail(request, year=None):
    queryset = models.Organization.objects.filter(is_active=True)
    serializer_class = serializers.OrganizationSerializer
