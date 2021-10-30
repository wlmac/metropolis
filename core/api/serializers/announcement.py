from django_grpc_framework import proto_serializers
from rest_framework import serializers

from core.api.serializers.custom import PrimaryKeyAndSlugRelatedField

from ... import models
from .. import api_pb2
from .tag import TagSerializer


class AnnouncementSerializer(proto_serializers.ModelProtoSerializer):
    author = PrimaryKeyAndSlugRelatedField(
        slug_field="username", queryset=models.User.objects.all()
    )
    organization = PrimaryKeyAndSlugRelatedField(
        slug_field="name", queryset=models.Organization.objects.all()
    )
    tags = TagSerializer(many=True)

    class Meta:
        model = models.Announcement
        proto_class = api_pb2.Announcement
        exclude = ["supervisor", "status", "rejection_reason"]
