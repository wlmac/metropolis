from rest_framework import serializers
from ... import models


class TimetableSerializer(serializers.Serializer):
    owner = serializers.SlugRelatedField(slug_field='username', queryset=models.User.objects.all())
    term = serializers.SlugRelatedField(slug_field='name', queryset=models.Term.objects.all())
    courses = serializers.SlugRelatedField(slug_field='code', queryset=models.Course.objects.all())