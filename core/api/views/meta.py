from django.conf import settings
from rest_framework import authentication, exceptions, parsers, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView


class APIVersion(APIView):
    def get(self, request):
        return Response({"version": settings.API_VERSION})
