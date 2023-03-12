from django.db.models import Count, Case, BooleanField, When
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from rest_framework import permissions, serializers

from ....models import Comment, User, Like
from .base import BaseProvider

typedir: dict[str, str] = {
    "blogpost": "core | blogpost",
    "announcement": "core | announcements",
}


class CommentSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    author = serializers.ReadOnlyField(source="author.id")
    edited = serializers.SerializerMethodField(read_only=True)
    children = serializers.SerializerMethodField(read_only=True)

    def get_likes(self, obj: Comment) -> int:
        return obj.likes.count()

    def get_children(self, obj: Comment) -> list[dict[str, bool]]:
        """
        Return a list of replies to this comment as a list of ids and have each show if they have replies.

        Returns:
            list: A list of dictionaries representing the replies to this comment. Each dictionary should contain
                  the keys "id" and "has_children", where "id" is the id of the reply and "has_children" is a boolean
                  indicating whether the reply has any children.
        """
        if (
            self.context["request"].user.has_perm("core.comment.view_flagged")
            or self.context["request"].user.is_staff
        ):
            replies = (
                obj.get_children()
                .annotate(
                    child_count=Count("children"),
                    has_children=Case(
                        When(child_count__gt=0, then=True),
                        default=False,
                        output_field=BooleanField(),
                    ),
                )
                .values("id", "has_children")
            )

        else:
            replies = (
                obj.get_children()
                .filter(live=True)
                .annotate(
                    child_count=Count("children"),
                    has_children=Case(
                        When(child_count__gt=0, then=True),
                        default=False,
                        output_field=BooleanField(),
                    ),
                )
                .values("id", "has_children")
            )
        return replies

    @staticmethod
    def get_edited(obj: Comment):
        print(obj.last_modified, obj.created_at)
        return obj.last_modified != obj.created_at

    def update(self, instance: Comment, validated_data) -> Comment:
        if instance.body != validated_data.get(
            "body", instance.body
        ):  # if change is  to body.
            instance.last_modified = timezone.now()
        super().update(instance, validated_data)
        return Response(instance, status=status.HTTP_200_OK)

    @staticmethod
    def delete(instance: Comment):
        instance.delete(force=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

    class Meta:
        model = Comment
        ordering = ["-likes"]
        fields = [
            "id",
            "author",
            "body",
            "created_at",
            "likes",
            "edited",
            "children",
        ]


class CommentNewSerializer(CommentSerializer):
    def create(self, validated_data) -> Comment:
        com = Comment()
        print(validated_data)  # todo remove

        keys = self.Meta.fields
        user: User = self.context["request"].user
        validated_data["author"] = user
        for key in keys:
            setattr(com, key, validated_data[key])
        if user.is_staff:  # bypass moderation if user is staff.
            com.live = True
        com.save()
        return Response(com, status=status.HTTP_201_CREATED)

    class Meta:
        model = Comment
        permission_classes = [IsAuthenticated]
        fields = [
            "content_type",
            "object_id",  # obj id of the blogpost or announcement.
            "body",
            "parent",
            "author",
        ]

class CommentProvider(BaseProvider):
    model = Comment
    allow_list = False

    @property
    def permission_classes(self):
        return [permissions.IsAuthenticated]

    @property
    def serializer_class(self):
        return dict(
            new=CommentNewSerializer,
        ).get(self.request.kind, CommentSerializer)

    def get_queryset(self, request):
        if request.user.has_perm("core.comment.view_flagged") or request.user.is_staff:
            return Comment.objects.all()
        return Comment.objects.filter(live=True)

    def get_last_modified(self, view):
        return (
            LogEntry.objects.filter(
                content_type=ContentType.objects.get(app_label="core", model="comment")
            )  # todo get ken to look at this.
            .filter(object_id=str(view.get_object().pk))
            .latest("action_time")
            .action_time
        )

    def get_last_modified_queryset(self):
        return (
            LogEntry.objects.filter(
                content_type=ContentType.objects.get(app_label="core", model="comment")
            )
            .latest("action_time")
            .action_time
        )


# ====================================================================================================
# -------------------------------------------  LIKES  -------------------------------------------
# ====================================================================================================


class LikeSerializer(serializers.ModelSerializer):
    def create(self, validated_data) -> Like:
        like = Like()
        keys = self.Meta.fields
        user: User = self.context["request"].user
        validated_data["author"] = user
        for key in keys:
            setattr(like, key, validated_data[key])
        like.save()
        return Response(like, status=status.HTTP_201_CREATED)

    class Meta:
        model = Like
        permission_classes = [IsAuthenticated]
        fields = [
            "content_type",
            "object_id",  # obj id of the blogpost or announcement.
            "author",
        ]


class LikeProvider(BaseProvider):
    model = Like
    allow_list = False

    @property
    def permission_classes(self):
        return [permissions.IsAuthenticated]

    @property
    def serializer_class(self):
        return LikeSerializer

    def get_last_modified(self, view):
        return (
            LogEntry.objects.filter(
                content_type=ContentType.objects.get(app_label="core", model="like")
            )
            .filter(object_id=str(view.get_object().pk))
            .latest("action_time")
            .action_time
        )

    def get_last_modified_queryset(self):
        return (
            LogEntry.objects.filter(
                content_type=ContentType.objects.get(app_label="core", model="like")
            )
            .latest("action_time")
            .action_time
        )
