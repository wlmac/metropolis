from datetime import datetime
from typing import Dict

from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView


class APIVersion(APIView):
    def get(self, request):
        return Response({"version": settings.API_VERSION})


class Banners(APIView):
    noncensored_keys = ("start", "end", "content", "icon_url", "cta_link", "cta_label")
    allowed_blank = ("icon_url", "cta_link", "cta_label")

    @classmethod
    def censor(cls, banner: Dict) -> Dict:
        res = {}
        for key in cls.noncensored_keys:
            if key in banner:
                res[key] = banner[key]
            elif key not in banner and key in cls.allowed_blank:
                pass
            else:
                raise KeyError(f"Required Key {key} not found in banner {banner}")
        return res

    @staticmethod
    def get(request):
        return Response(Banners.calculate_banners)

    @classmethod
    def calculate_banners(cls):
        now = datetime.now(settings.TZ)
        current = filter(lambda b: b["start"] < now < b["end"], settings.BANNER3)
        current = list(map(Banners.censor, current))
        upcoming = filter(lambda b: now <= b["start"], settings.BANNER3)
        upcoming = list(map(Banners.censor, upcoming))
        return dict(current=current, upcoming=upcoming)
