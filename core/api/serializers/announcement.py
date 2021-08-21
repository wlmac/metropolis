from rest_framework import serializers
from ... import models


class AnnouncementSerializer(serializers.Serializer):
    author = serializers.SlugRelatedField(slug_field='username', allow_null=True, queryset=models.User.objects.all())
    created_date = serializers.DateTimeField()
    last_modified_date = serializers.DateTimeField()

    title = serializers.CharField(max_length=128, allow_blank=True)
    body = serializers.CharField(allow_blank=True, style={'base_template': 'textarea.html'})
    tags = serializers.SlugRelatedField(slug_field='name', many=True, queryset=models.Tag.objects.all())

    organization = serializers.SlugRelatedField(slug_field='name', queryset=models.Organization.objects.all())

    is_public = serializers.BooleanField(default=True)
    supervisor = serializers.SlugRelatedField(slug_field='username', allow_empty=True, allow_null=True, queryset=models.User.objects.all())
    status = serializers.ChoiceField(models.announcement_status_choices, default='p')
    rejection_reason = serializers.CharField(max_length=140, allow_blank=True)
