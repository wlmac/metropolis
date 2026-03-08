from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from ...models import Banner


@extend_schema(
    description="Returns the current API version.",
    responses={200: {"version": "string"}},
    examples=[
        OpenApiExample(
            name="APIVersion",
            response_only=True,
            status_codes=[200],
            value={"version": "3.2.1"},
        )
    ],
)
class APIVersion(APIView):
    """Returns the current API version."""

    @staticmethod
    def get(request) -> dict[str, str]:
        return Response({"version": settings.API_VERSION})


@extend_schema(
    description="Returns the current banners and upcoming banners for the home page. note: upcoming banners only return the banners for the next day.",
    responses={
        200: {
            "start": "string",
            "end": "string",
            "content": "string",
            "icon_url": "string",
            "cta_link": "string",
            "cta_label": "string",
        }
    },
    examples=[
        OpenApiExample(
            name="Banners",
            response_only=True,
            status_codes=[200],
            value={
                "start": "2024-02-05T21:49:50.361170-05:00",
                "end": "2024-02-10T21:49:50.361170-05:00",
                "content": "Hello! This is a cool banner!",
                "icon_url": "/static/core/img/logo/logo-maskable-192.png",
                "cta_link": "https://portfolio-cqctxs.vercel.app/",
                "cta_label": "Hmmm...",
            },
        )
    ],
)
class Banners(APIView):
    @staticmethod
    def get(request):
        """Returns the current banners and upcoming banners for the home page. note: upcoming banners only return the banners for the next day"""
        return Response(Banners.calculate_banners())

    @classmethod
    def calculate_banners(cls):
        now = timezone.now()

        fields = [f.name for f in Banner._meta.fields if f.name != "name"]

        current = Banner.objects.filter(start_date__lte=now, end_date__gt=now).values(
            *fields
        )
        upcoming = Banner.objects.filter(
            start_date__gt=now, start_date__lt=now + timedelta(days=1)
        ).values(*fields)

        return dict(current=list(current), upcoming=list(upcoming))
