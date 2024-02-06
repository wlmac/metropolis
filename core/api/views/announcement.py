from oauth2_provider.contrib.rest_framework import TokenHasScope
from rest_framework import permissions

from .. import serializers
from ..utils import ListAPIViewWithFallback
from ... import models

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework.decorators import api_view
from core.api.serializers.announcement import AnnouncementSerializer

@extend_schema(
    responses={200: AnnouncementSerializer(many=True)},
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
class AnnouncementListAll(ListAPIViewWithFallback):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.AnnouncementSerializer

    def get_queryset(self):
        return models.Announcement.get_all(user=self.request.user)

@extend_schema(
    responses={200: AnnouncementSerializer(many=True)},
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
class AnnouncementListMyFeed(ListAPIViewWithFallback):
    permission_classes = [permissions.IsAuthenticated | TokenHasScope]
    required_scopes = ["me_ann"]
    serializer_class = serializers.AnnouncementSerializer

    def get_queryset(self):
        return self.request.user.get_feed()