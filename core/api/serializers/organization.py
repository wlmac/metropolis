from rest_framework import serializers
from ... import models


class OrganizationSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    owner = serializers.SlugRelatedField(slug_field='username', allow_null=True, queryset=models.User.objects.all())
    supervisors = serializers.SlugRelatedField(slug_field='username', allow_null=True, many=True, queryset=models.User.objects.all())
    execs = serializers.SlugRelatedField(slug_field='username', allow_null=True, many=True, queryset=models.User.objects.all())

    name = serializers.CharField(max_length=64)
    description = serializers.CharField(allow_blank=True, style={'base_template': 'textarea.html'})

    registered_date = serializers.DateTimeField()
    is_open = serializers.BooleanField(default=True)
    tags = serializers.SlugRelatedField(slug_field='name', many=True, queryset=models.Tag.objects.all())