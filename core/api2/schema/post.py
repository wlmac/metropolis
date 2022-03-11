from datetime import datetime
from typing import Optional

import graphene
from django.db.models import Q
from graphene_django import DjangoObjectType

from ...models import Announcement, BlogPost


class StatusType(graphene.Enum):
    PENDING_APPROVAL = 1
    APPROVED = 2
    REJECTED = 3

    @classmethod
    def db_status(cls, self):
        if self == cls.APPROVED:
            return "a"
        elif self == cls.PENDING_APPROVAL:
            return "p"
        elif self == cls.REJECTED:
            return "r"
        else:
            raise Exception("Invalid status")


class AnnouncementType(DjangoObjectType):
    in_feed = graphene.Boolean()
    status = graphene.Field(StatusType)

    def resolve_rejection_reason(self, info):
        assert info.context.user.is_authenticated, "not authenticated"
        assert (
            info.context.user.is_superuser
            or Announcement.objects.filter(
                Q(organization__owner=info.context.user)
                | Q(organization__execs=info.context.user)
                | Q(organization__supervisors=info.context.user)
            ).exists()
        ), "insufficient permissions"
        return self.rejection_reason

    def resolve_in_feed(self, info):
        return Announcement.objects.filter(
            Q(is_public=True, tags__follower=info.context.user)
            | Q(organization__member=info.context.user)
        ).exists()

    def resolve_status(self, info):
        if self.status == "a":
            return StatusType.APPROVED
        elif self.status == "p":
            return StatusType.PENDING_APPROVAL
        elif self.status == "r":
            return StatusType.REJECTED
        else:
            raise Exception("Invalid status")

    class Meta:
        model = Announcement


class BlogPostType(DjangoObjectType):
    class Meta:
        model = BlogPost


class Schema:
    announcements = graphene.List(
        AnnouncementType,
        is_public=graphene.Boolean(),
        in_feed=graphene.Boolean(),
        status=graphene.Argument(StatusType),
    )
    blog_posts = graphene.List(
        BlogPostType,
        is_published=graphene.Boolean(),
        created_after=graphene.DateTime(),
    )

    def resolve_announcements(
        self,
        info,
        is_public: Optional[bool] = None,
        in_feed: Optional[bool] = None,
        status: Optional[StatusType] = None,
    ):
        if in_feed is not None:
            assert (
                info.context.user.is_authenticated
            ), "Authentication required for inFeed"

        q = Announcement.objects.filter(
            **({"is_public": is_public} if is_public is not None else {}),
            **({"status": StatusType.db_status(status)} if status is not None else {}),
        )
        if in_feed is True:
            q.filter(
                Q(is_public=True, tags__follower=info.context.user)
                | Q(organization__member=info.context.user)
            )
        elif in_feed is False:
            raise Exception("Must be authenticated in to filter by in_feed")
            q.exclude(
                Q(is_public=True, tags__follower=info.context.user)
                | Q(organization__member=info.context.user)
            )
        if status != StatusType.APPROVED:
            q.filter(
                Q(organization__member=info.context.user)
                | Q(organization__supervisors=info.context.user)
                | Q(organization__execs=info.context.user)
                | Q(organization__owner=info.context.user)
            )
            pass
        return q.distinct().all()

    def resolve_blog_posts(
        self,
        info,
        is_published: Optional[bool] = None,
        created_after: Optional[datetime] = None,
    ):
        if is_published in (None, False):
            assert (
                info.context.user.is_authenticated
            ), "Authentication required for inFeed"
            assert info.context.user.is_superuser, "insufficient permissions"
        return BlogPost.objects.filter(
            **({"is_published": is_published} if is_published is None else {}),
            **(
                {"created_date__gte": created_after}
                if created_after is not None
                else {}
            ),
        )
