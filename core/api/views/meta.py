from rest_framework import authentication, exceptions, parsers, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.conf import settings


class APIVersion(APIView):
    def get(self, request):
        return Response({"version": settings.API_VERSION})
