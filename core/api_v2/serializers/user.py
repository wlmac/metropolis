from rest_framework import serializers

from .tag import TagSerializer
from ... import models


class UserSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=models.Tag.objects.all())
    organizations = serializers.SlugRelatedField(slug_field='name', many=True,
                                                 queryset=models.Organization.objects.all())
    tags_following = TagSerializer(many=True)

    class Meta:
        model = models.User
        fields = ['username', 'first_name', 'last_name', 'bio', 'timezone', 'graduating_year', 'organizations',
                  'tags_following']
