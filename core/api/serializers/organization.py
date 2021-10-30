from django_grpc_framework import proto_serializers
from rest_framework import serializers

from core.api.serializers.custom import PrimaryKeyAndSlugRelatedField

from ... import models
from .. import api_pb2
from .tag import TagSerializer


class OrganizationSerializer(proto_serializers.ModelProtoSerializer):
    owner = PrimaryKeyAndSlugRelatedField(
        slug_field="username", queryset=models.User.objects.all()
    )
    supervisors = PrimaryKeyAndSlugRelatedField(
        slug_field="username", many=True, queryset=models.User.objects.all()
    )
    execs = PrimaryKeyAndSlugRelatedField(
        slug_field="username", many=True, queryset=models.User.objects.all()
    )

    tags = TagSerializer(many=True)

    class Meta:
        model = models.Organization
        proto_class = api_pb2.Organization
        fields = "__all__"
