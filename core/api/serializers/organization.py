from rest_framework import serializers
from ... import models


class OrganizationSerializer(serializers.Serializer):
    owner = serializers.SlugRelatedField(slug_field='username', allow_null=True)
    supervisors = serializers.SlugRelatedField(slug_field='username', allow_null=True, many=True)
    execs = serializers.SlugRelatedField(slug_field='username', allow_null=True, many=True)

    name = serializers.CharField(max_length=64)
    description = serializers.CharField(allow_blank=True)

    registered_date = serializers.DateTimeField()
    is_open = serializers.BooleanField(default=True)
    tags = serializers.SlugRelatedField(slug_field='name', many=True)