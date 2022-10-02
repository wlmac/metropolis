from django.utils import timezone
from rest_framework import  permissions
from rest_framework import serializers

from .... import models
from .base import BaseProvider


class Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "bio",
            "timezone",
            "graduating_year",
            "organizations",
            "tags_following",
        ]


class Provider(BaseProvider):
    serializer_class = Serializer
    model = models.User
    allow_list = False

    @property
    def permission_classes(self):
        return [permissions.DjangoModelPermissions] if self.request.mutate else [permissions.IsAuthenticated]

    def get_queryset(self, request):
        return models.User.objects.all()

    def get_last_modified(self, view):
        return timezone.now()

    def get_last_modified_queryset(self):
        return timezone.now()
