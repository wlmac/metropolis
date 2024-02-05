from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from rest_framework import permissions, serializers

from .base import BaseProvider
from core.api.serializers.custom import (
    TagRelatedField,
    CommentField,
    LikeField,
    SingleUserField,
)
from core.models import BlogPost


class Serializer(serializers.ModelSerializer):
    likes = LikeField()
    comments = CommentField()
    author = SingleUserField()
    tags = TagRelatedField()

    def to_representation(self, instance: BlogPost):
        request = self.context["request"]
        if (
            request.mutate is False and request.detail
        ):  # detail is True and mutate is False meaning we are retrieving an object
            instance.increment_views()
        return super().to_representation(instance)

    class Meta:
        model = BlogPost
        ordering = ["-created_date"]
        fields = [
            "id",
            "slug",
            "title",
            "body",
            "author",
            "views",
            "created_date",
            "last_modified_date",
            "featured_image",
            "featured_image_description",
            "is_published",
            "tags",
            "likes",
            "comments",
        ]


class BlogPostProvider(BaseProvider):
    model = BlogPost
    additional_lookup_fields = ["slug"]
    raw_serializers = {
        "_": Serializer
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def permission_classes(self):
        return (
            [permissions.DjangoModelPermissions]
            if self.request.mutate
            else [permissions.AllowAny]
        )

    def get_queryset(self, request):
        if request.user.has_perm("core.blog_post.view") or request.user.is_superuser:
            return BlogPost.objects.filter(is_archived=False)
        else:
            return BlogPost.public()

    def get_last_modified(self, view):
        return view.get_object().last_modified_date

    def get_last_modified_queryset(self):
        return (
            LogEntry.objects.filter(
                content_type=ContentType.objects.get(app_label="core", model="blogpost")
            )
            .latest("action_time")
            .action_time
        )
