from django.utils import timezone
from rest_framework import permissions, serializers

from core.api.serializers.custom import (
    CommentField,
    LikeField,
    SingleUserField,
    TagRelatedField,
)
from core.models import Exhibit

from .base import BaseProvider


class Serializer(serializers.ModelSerializer):
    likes = LikeField()
    comments = CommentField()
    tags = TagRelatedField()
    author = SingleUserField()

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
    additional_lookup_fields = ["slug"]
    raw_serializers = {"_": Serializer}

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
