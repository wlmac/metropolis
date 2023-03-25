from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from rest_framework import permissions, serializers

from .base import BaseProvider
from ...utils.posts import likes, comments
from ....models import BlogPost


class Serializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)

    def to_representation(self, instance: BlogPost):
        request = self.context["request"]
        if request.mutate is False and request.detail:  # detail is True and mutate is False when we are retrieving an object
            instance.increment_views()
        return super().to_representation(instance)

    def get_likes(self, obj: BlogPost) -> int:
        return likes(obj)

    def get_comments(self, obj: BlogPost):
        return comments(self.context, obj)

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
    serializer_class = Serializer
    model = BlogPost

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
            return BlogPost.objects.all()
        else:
            return BlogPost.objects.filter(is_published=True)

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
