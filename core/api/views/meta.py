from typing import Dict

from django.conf import settings
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView


class APIVersion(APIView):
    def get(self, request):
        return Response({"version": settings.API_VERSION})


class Banners(APIView):
    noncensored_keys = ("start", "end", "content", "icon_url", "cta_link", "cta_label")

    @classmethod
    def censor(cls, banner: Dict) -> Dict:
        res = {}
        if "icon_url" not in banner:
            banner["icon_url"] = settings.THEME_LOGO
        for key in cls.noncensored_keys:
            res[key] = banner[key]
        return res

    @staticmethod
    def get(request):
        now = timezone.now()
        current = filter(lambda b: b["start"] < now < b["end"], settings.BANNER3)
        current = list(map(Banners.censor, current))
        upcoming = filter(lambda b: now <= b["start"], settings.BANNER3)
        upcoming = list(map(Banners.censor, upcoming))
        return Response(dict(current=current, upcoming=upcoming))
