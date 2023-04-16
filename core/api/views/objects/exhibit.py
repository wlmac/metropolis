from django.utils import timezone
from rest_framework import permissions, serializers

from .base import BaseProvider
from ...utils.posts import likes, comments
from ....models import Exhibit


class Serializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)

    def get_likes(self, obj: Exhibit) -> int:
        return likes(obj)

    def get_comments(self, obj: Exhibit):
        return comments(self.context, obj)

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
    serializer_class = Serializer
    model = Exhibit
    lookup_fields = ["id", "slug"]

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

    def get_last_modified(self, view):
        return view.get_object().last_modified_date

    def get_last_modified_queryset(self):
        return Exhibit.objects.latest("last_modified_date").last_modified_date
