from rest_framework import generics

from .. import serializers
from ..utils import ListAPIViewWithFallback
from ... import models


class OrganizationList(ListAPIViewWithFallback):
    queryset = models.Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer


class OrganizationDetail(generics.RetrieveAPIView):
    queryset = models.Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer
