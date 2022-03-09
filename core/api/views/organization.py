from rest_framework import generics

from ... import models
from .. import serializers
from .fallback import ListAPIViewWithFallback


class OrganizationList(ListAPIViewWithFallback):
    queryset = models.Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer


class OrganizationDetail(generics.RetrieveAPIView):
    queryset = models.Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer
