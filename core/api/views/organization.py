from .. import serializers
from rest_framework import generics, permissions
from rest_framework.views import APIView
from ... import models
from rest_framework.response import Response


class OrganizationList(generics.ListAPIView):
    queryset = models.Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer


class OrganizationDetail(generics.RetrieveAPIView):
    queryset = models.Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer
