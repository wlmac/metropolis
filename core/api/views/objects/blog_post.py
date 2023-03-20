from typing import Dict, List
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Case, When, BooleanField
from rest_framework import permissions, serializers

from .base import BaseProvider
from ...utils.posts import likes
from ....models import BlogPost


class Serializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)

    def to_representation(self, instance: BlogPost):
        instance.increment_views()
        return super().to_representation(instance)

    def get_likes(self, obj: BlogPost) -> int:
        return likes(obj)

    def get_comments(self, obj: BlogPost) -> List[Dict[str, bool]]:
        # return a list of comments for this blog post as a tuple of ids and have each show if they have replies.
        # check if the user has the comments.preview permission
        if (
            self.context["request"].user.has_perm("core.comment.view_flagged")
            or self.context["request"].user.is_superuser
        ):
            queryset = obj.comments.all()
        else:
            queryset = obj.comments.filter(live=True)

        comments = (
            queryset.annotate(
                child_count=Count("children"),
                has_children=Case(
                    When(child_count__gt=0, then=True),
                    default=False,
                    output_field=BooleanField(),
                ),
                likeCount=Case(
                    When(likes__isnull=True, then=0),
                    default=Count("likes"),
                ),
            )
            .values("id", "has_children", "body", "author", "likeCount")
            .order_by("-likeCount")
        )
        return comments

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
