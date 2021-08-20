from rest_framework import serializers
from ... import models


class TimetableSerializer(serializers.Serializer):
    owner = serializers.SlugRelatedField(slug_field='username')
    term = serializers.SlugRelatedField(slug_field='name')
    courses = serializers.SlugRelatedField(slug_field='code')