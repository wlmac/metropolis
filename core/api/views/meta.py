from datetime import timedelta
from typing import Dict

from django.conf import settings
from django.utils import timezone
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView


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
    def get(request) -> Dict[str, str]:
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
    uncensored_keys = ("start", "end", "content", "icon_url", "cta_link", "cta_label")
    allowed_blank = ("icon_url", "cta_link", "cta_label")

    @classmethod
    def censor(cls, banner: Dict) -> Dict:
        res = {}
        for key in cls.uncensored_keys:
            if key in banner:
                res[key] = banner[key]
            elif key not in banner and key in cls.allowed_blank:
                pass
            else:
                raise KeyError(f"Required Key {key} not found in banner {banner}")
        return res

    @staticmethod
    def get(request):
        """Returns the current banners and upcoming banners for the home page. note: upcoming banners only return the banners for the next day"""
        return Response(Banners.calculate_banners())

    @classmethod
    def calculate_banners(cls):
        now = timezone.now()
        current = filter(lambda b: b["start"] <= now < b["end"], settings.BANNER3)
        current = list(map(Banners.censor, current))
        upcoming = filter(
            lambda b: now < b["start"] > now + timedelta(days=1), settings.BANNER3
        )
        upcoming = list(map(Banners.censor, upcoming))
        return dict(current=current, upcoming=upcoming)
