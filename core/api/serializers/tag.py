from rest_framework import serializers
from ... import models


class TagSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30)
    description = serializers.CharField(allow_blank=True)