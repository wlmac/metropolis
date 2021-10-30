from django_grpc_framework import proto_serializers
from rest_framework import serializers

from ... import models
from .. import api_pb2


class TagSerializer(proto_serializers.ModelProtoSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=models.Tag.objects.all())

    class Meta:
        model = models.Tag
        proto_class = api_pb2.Tag
        fields = ["id", "name", "color"]
