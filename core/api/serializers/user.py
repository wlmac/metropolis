from rest_framework import serializers
from django_grpc_framework import proto_serializers

from ... import models
from .. import api_pb2
from .tag import TagSerializer


class UserSerializer(proto_serializers.ModelProtoSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=models.Tag.objects.all())
    organizations = serializers.SlugRelatedField(
        slug_field="name", many=True, queryset=models.Organization.objects.all()
    )
    tags_following = TagSerializer(many=True)

    class Meta:
        model = models.User
        proto_class = api_pb2.User
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
