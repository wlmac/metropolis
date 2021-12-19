from rest_framework import generics

from ... import models
from .. import serializers


class OrganizationList(generics.ListAPIView):
    queryset = models.Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer


class OrganizationDetail(generics.RetrieveAPIView):
    queryset = models.Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer
