from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from rest_framework import permissions, serializers

from ....models import Comment, User
from .base import BaseProvider

typedir: dict[str, str] = {
    "blogpost": "core | blogpost",
    "announcement": "core | announcements",
}


class CommentSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    likes = serializers.IntegerField(read_only=True)
    author = serializers.ReadOnlyField(source="author.id")
    edited = serializers.SerializerMethodField()

    def get_edited(self, obj: Comment):
        return obj.last_modified != obj.created_at

    def get_children(self, obj):
        # check if the user has the comments.preview permission
        if (
            self.context["request"].user.has_perm("core.comment.view_flagged")
            or self.context["request"].user.is_staff
        ):
            return obj.children.all().values_list(
                "id", flat=True
            )  # todo handle children's children
        return obj.children.filter(live=True).values_list("id", flat=True)

    def update(self, instance: Comment, validated_data) -> Comment:
        if instance.body != validated_data.get(
            "body", instance.body
        ):  # changes to body.
            instance.last_modified = timezone.now()
        super().update(instance, validated_data)
        return Response(instance, status=status.HTTP_200_OK)

    @staticmethod
    def delete(instance: Comment):
        instance.delete(force=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

    class Meta:
        model = Comment
        ordering = ["likes"]
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
        print(validated_data)

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
        permission_classes = [IsAuthenticated]  # todo this valid?
        fields = [
            "content_type",
            "object_id",  # obj id of the blogpost or announcement.
            "body",
            "parent",
            "author",
        ]


class CommentListSerializer(CommentSerializer):
    replies = serializers.SerializerMethodField()
    edited = serializers.SerializerMethodField()

    def get_queryset(self, request):
        if request.user.has_perm("core.comment.view_flagged") or request.user.is_staff:
            return Comment.objects.all().order_by("-likes")
        return Comment.objects.filter(live=True).order_by("-likes")

    def get_replies(self, obj: Comment):
        if obj.bottom_lvl:
            return []
        return obj.children.all()

    class Meta:
        model = Comment
        fields = [
            "id",
            "author",
            "body",
            "created_at",
            "edited",
            "likes",
            "replies",
        ]


class CommentProvider(BaseProvider):
    model = Comment

    @property
    def permission_classes(self):
        return [permissions.IsAuthenticated]

    @property
    def serializer_class(self):
        return dict(
            new=CommentNewSerializer,
            list=CommentListSerializer,
        ).get(self.request.kind, CommentSerializer)

    def get_queryset(self, request):
        if request.user.has_perm("core.comment.view_flagged") or request.user.is_staff:
            return Comment.objects.all()
        return Comment.objects.filter(live=True)

    def get_last_modified(self, view):
        return (
            LogEntry.objects.filter(
                content_type=ContentType.objects.get(app_label="core", model="comment")
            )  # todo this might not workkkkkkkk
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


class CommentRepliesAPIView(generics.ListAPIView):
    """# todo impl to v3 or (just impl into detail with a is_top_lvl flag)
    List all replies for a given comment
    """

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        comment_id = self.kwargs.get("pk")
        queryset = Comment.objects.filter(
            parent_id=comment_id,
            live=True,
        ).order_by("created_at")
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
