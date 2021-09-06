from rest_framework import serializers
from .tag import TagSerializer
from ... import models


class AnnouncementSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', queryset=models.User.objects.all())
    organization = serializers.SlugRelatedField(slug_field='name', queryset=models.Organization.objects.all())
    tags = TagSerializer(many=True)

    class Meta:
        model = models.Announcement
        exclude = ['supervisor', 'status', 'rejection_reason']
