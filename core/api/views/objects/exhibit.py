from django.utils import timezone
from rest_framework import permissions, serializers

from .base import BaseProvider
from ...serializers.custom import (
    TagRelatedField,
    AuthorField,
    LikeField,
    CommentField,
)
from ....models import Exhibit


class Serializer(serializers.ModelSerializer):
    likes = LikeField()
    comments = CommentField()
    tags = TagRelatedField()
    author = AuthorField()

    class Meta:
        model = Exhibit
        ordering = ["-created_date"]
        fields = [
            "id",
            "slug",
            "title",
            "author",
            "created_date",
            "last_modified_date",
            "content",
            "content_description",
            "is_published",
            "show_after",
            "tags",
            "likes",
            "comments",
        ]


class ExhibitProvider(BaseProvider):
    model = Exhibit
    lookup_fields = ["id", "slug"]
    serializer_class = Serializer

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
        if request.user.has_perm("core.exhibit.view") or request.user.is_superuser:
            return Exhibit.objects.all()
        else:
            return Exhibit.objects.filter(
                is_published=True, show_after__lte=timezone.now()
            )

    @staticmethod
    def get_last_modified(view):
        return view.get_object().last_modified_date

    @staticmethod
    def get_last_modified_queryset():
        return Exhibit.objects.latest("last_modified_date").last_modified_date
