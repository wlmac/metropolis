from abc import ABC

from rest_framework import serializers

from core.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    likes = serializers.IntegerField(read_only=True)
    author = serializers.ReadOnlyField(source='author.id')

    def get_children(self, obj):
        # check if the user has the comments.preview permission
        if self.context['request'].user.has_perm("core.comments.preview") or self.context['request'].user.is_superuser:
            return obj.children.all().values_list('id', flat=True)
        return obj.children.filter(live=True).values_list('id', flat=True)

    class Meta:
        model = Comment
        ordering = ["likes"]
        fields = ['id', 'author', 'body', 'created_at', 'last_modified', 'likes', 'children']


class CommentListSerializer(serializers.ListSerializer, ABC):
    id = serializers.IntegerField(source='pk')
    is_top_level = serializers.BooleanField()

    def to_representation(self, instance):
        is_top_level = instance.is_top_level
        # only return live=True comments if the user doesn't have the comments.preview permission
        if not self.context['request'].user.has_perm("core.comments.preview") or not self.context['request'].user.is_superuser:
            if not instance.live:
                return

        return {
            'id': instance.pk,
            'is_top_level': is_top_level,
        }
