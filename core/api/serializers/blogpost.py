from rest_framework import serializers

from core.api.serializers.custom import PrimaryKeyAndSlugRelatedField

from ... import models
from .tag import TagSerializer


class BlogPostSerializer(serializers.ModelSerializer):
    author = PrimaryKeyAndSlugRelatedField(
        slug_field="username", queryset=models.User.objects.all()
    )
    tags = TagSerializer(many=True)

    class Meta:
        model = models.BlogPost
        exclude = ["is_published"]
