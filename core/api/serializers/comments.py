from rest_framework import permissions, serializers
from rest_framework.serializers import ListSerializer

from core.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all())
    owner = PrimaryKeyAndSlugRelatedField(
        slug_field="username", queryset=models.User.objects.all()
    )
    term = TermSerializer()
    courses = CourseSerializer(many=True)

    class Meta:
        model = Comment
        fields = ["id", "body", "author", "get_children", "created_at", "last_modified", "likes"]


class CommentListSerializer(ListSerializer):
    ...
