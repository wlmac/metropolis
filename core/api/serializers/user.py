from rest_framework import serializers
from ... import models

class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    bio = serializers.CharField(required=False, allow_blank=True)
    timezone = serializers.ChoiceField(models.timezone_choices, default="UTC")
    graduating_year = serializers.ChoiceField(models.graduating_year_choices, allow_null=True)
    organizations = serializers.SlugRelatedField(slug_field='name', many=True, queryset=models.Organization.objects.all())
    tags_following = serializers.SlugRelatedField(slug_field='name', many=True, queryset=models.Tag.objects.all())
