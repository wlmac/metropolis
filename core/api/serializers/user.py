from rest_framework import serializers
from ... import models
from .tag import TagSerializer


class UserSerializer(serializers.ModelSerializer):
    organizations = serializers.SlugRelatedField(slug_field='name', many=True, queryset=models.Organization.objects.all())
    tags_following = TagSerializer(many=True)

    class Meta:
        model = models.User
        fields = ['username', 'first_name', 'last_name', 'bio', 'timezone', 'graduating_year', 'organizations', 'tags_following']
