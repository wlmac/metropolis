from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone
from oauth2_provider.contrib.rest_framework import TokenHasScope
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .. import serializers, utils
from ..utils import ListAPIViewWithFallback
from ... import models

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework.decorators import api_view
from core.api.serializers.timetable import TimetableSerializer


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

@extend_schema(
    responses={200: TimetableSerializer(many=True)},
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
def timetableList(request, year=None):
    permission_classes = [permissions.IsAuthenticated | TokenHasScope]
    required_scopes = ["me_timetable"]
    serializer_class = serializers.TimetableSerializer

    def get_queryset(self):
        return models.Timetable.objects.filter(
            owner=self.request.user,
            term__end_date__gte=(timezone.now() - settings.TERM_GRACE_PERIOD),
        )

@extend_schema(
    responses={200: TimetableSerializer(many=True)},
)
@api_view(["GET"])
def timetableSchedule(request, year=None):
    permissions_classes = [permissions.IsAuthenticated | TokenHasScope]
    required_scopes = ["me_timetable", "me_schedule"]

    def get(self, request, pk):
        timetable = get_object_or_404(models.Timetable, pk=pk)

        if request.user != timetable.owner:
            return Response({}, status=status.HTTP_403_FORBIDDEN)

        date = utils.parse_date_query_param(request)

        return Response(timetable.day_schedule(target_date=date))

@extend_schema(
    responses={200: TimetableSerializer(many=True)},
)
@api_view(["GET"])
def timetableDetails(request, year=None):
    permission_classes = [IsOwner]
    queryset = models.Timetable.objects.filter(
        term__end_date__gte=(timezone.now() - settings.TERM_GRACE_PERIOD)
    )
    serializer_class = serializers.TimetableSerializer
