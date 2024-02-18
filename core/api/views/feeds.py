from django.conf import settings
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView


@extend_schema(
    description="Returns announcement feeds.",
    responses={200: {"announcements": []}},
    examples=[
        OpenApiExample(
            name="Feeds",
            response_only=True,
            status_codes=[200],
            value=[{"announcement1": "placeholder"}, {"announcement2": "placeholder"}],
        )
    ],
)
class Feeds(APIView):
    """Returns Announcement feeds."""

    @staticmethod
    def get(request):
        return Response(list(settings.ANNOUNCEMENTS_CUSTOM_FEEDS))
