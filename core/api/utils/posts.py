from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.contenttypes.models import ContentType
from django.db.models import (
    Subquery,
    Count,
    Case,
    BooleanField,
    When,
    OuterRef,
    QuerySet,
)
from django.db.models.functions import Coalesce

from core.models import Like

if TYPE_CHECKING:
    from core.models import BlogPost, Announcement, Comment


def likes(obj: "BlogPost" | "Announcement" | "Comment") -> int:
    c_type = ContentType.objects.get_for_model(obj.__class__)
    count = Like.objects.filter(object_id=obj.id, content_type=c_type).count()
    return count


def comments(
    context, obj: "BlogPost" | "Announcement" | "Comment", replies: bool = False
) -> QuerySet[Comment]:
    """
    args:
        context: context from the view
        obj: the object to get comments for
        replies: if True, use obj.get_children() if False, use obj.comments... (default False)

    Returns a QuerySet (List) of comments for a given post.
    If the user is not a superuser or has the view_flagged permission, only live comments will be returned.
    """
    if (
        context["request"].user.has_perm("core.comment.view_flagged")
        or context["request"].user.is_superuser
    ):
        queryset = obj.get_children(su=True) if replies else obj.comments.all()
    else:
        queryset = obj.get_children() if replies else obj.comments.filter(live=True)

    like_count = Coalesce(
        Subquery(
            Like.objects.filter(object_id=OuterRef("id"), content_type__model="comment")
            .values("object_id")
            .annotate(count=Count("id"))
            .values("count")[:1]
        ),
        0,
    )

    comment_set = (
        queryset.annotate(
            child_count=Count("children"),
            has_children=Case(
                When(child_count__gt=0, then=True),
                default=False,
                output_field=BooleanField(),
            ),
            likes=like_count,
        )
        .values("id", "has_children", "body", "author", "likes")
        .order_by("-likes")
    )
    return comment_set
