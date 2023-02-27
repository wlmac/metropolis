from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from ..serializers.comments import CommentSerializer, CommentListSerializer
from ..utils.permissions import IsStaffOrAuthor
from ...models import Comment

typedir: dict[str, str] = {
    "blogpost": "core | blogpost",
    "announcement": "core | announcements",
}


class CommentDetail:
    ...


class CommentEditDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for editing and deleting a comment.
    """

    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated, IsStaffOrAuthor]

    def perform_update(self, serializer):
        serializer.save(last_modified=timezone.now())

    def perform_destroy(self, instance):
        print("perform_destroy" "instance: ", instance, type(instance), instance.id)
        instance.delete(force=True)


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        content_type = typedir.get(self.kwargs.get("type"), None)
        if content_type is None:
            return Response(
                {
                    "error": "Invalid content type make sure it's 'blog' or 'announcement'"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        obj = Comment.objects.create(
            author=self.request.user,
            content_type=content_type,
            object_id=self.kwargs.get("pk"),
            body=serializer.validated_data.get("body"),
        )
        obj.save()
        return Response(CommentSerializer(obj).data, status=status.HTTP_201_CREATED)


class CommentUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_staff:
            return queryset
        else:
            return queryset.filter(author=user)


@api_view(["GET"])
def comment_detail(request, pk):
    comment = get_object_or_404(Comment, pk=pk, live=True)

    serializer = CommentSerializer(comment)
    return Response(serializer.data)


class CommentListAPIView(generics.ListAPIView):
    """
    List all top-level comments for a given content object
    """

    serializer_class = CommentListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def dispatch(self, request, *args, **kwargs):
        if self.kwargs.get("type") not in ["blogpost", "announcement"]:
            return Response(
                {
                    "error": "Invalid content type make sure it's 'blogpost' or 'announcement'"
                },
                status=status.HTTP_400_BAD_REQUEST,
                content_type="application/json",
            )

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        content_type = ContentType.objects.filter(model=self.kwargs.get("type")).first()
        print("content_type: ", content_type, type(content_type))
        pk = self.kwargs.get("pk")
        print("pk: ", pk, type(pk))
        if content_type and pk:
            queryset = Comment.objects.filter(
                content_type=content_type,
                object_id=pk,
                live=True,
            ).order_by("-likes")
            return queryset
        else:
            return Comment.objects.none()

        # return Response(
        #    {"error": "Invalid content type or object id"},
        #    status=status.HTTP_400_BAD_REQUEST,
        # )


class CommentRepliesAPIView(generics.ListAPIView):
    """
    List all replies for a given comment
    """

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        comment_id = self.kwargs.get("pk")
        queryset = Comment.objects.filter(
            parent_id=comment_id,
            live=True,
        ).order_by("created")
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
