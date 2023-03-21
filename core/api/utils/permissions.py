from rest_framework.permissions import BasePermission


class IsAuthor(BasePermission):
    """
    Custom permission class to check if the user is superuser or the author of the post/comment.
    """

    def has_object_permission(self, request, view, obj):
        return any(
            [
                request.user.is_superuser
                or obj.author == request.user
                or obj.post.author == request.user
            ]
        )
