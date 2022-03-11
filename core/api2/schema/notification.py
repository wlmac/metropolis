from datetime import datetime
from typing import List, Optional

import graphene
from django.db.models import Q
from graphene_django import DjangoObjectType

from ...models import Announcement, BlogPost, Event
from .course import EventType
from .organization import OrganizationType
from .post import AnnouncementType, BlogPostType
from .user import UserType


class AnnouncementApprovalType(graphene.ObjectType):
    announcement = graphene.Field(AnnouncementType)


class EntityType(graphene.Union):
    class Meta:
        types = (UserType, OrganizationType)


class PayloadType(graphene.Union):
    class Meta:
        types = (AnnouncementType, AnnouncementApprovalType, BlogPostType, EventType)


class NotificationType(graphene.ObjectType):
    id = graphene.ID(required=True)
    target = graphene.Field(
        EntityType, description="If null, the target is the whole school."
    )
    payload = graphene.Field(PayloadType)
    start = graphene.DateTime()
    end = graphene.DateTime()


class Schema:
    notifications = graphene.List(
        NotificationType, start=graphene.DateTime(), end=graphene.DateTime()
    )

    def resolve_notifications(
        self, info, start: Optional[datetime] = None, end: Optional[datetime] = None
    ):
        assert info.context.user.is_authenticated, "must be authenticated"
        notifs: List[NotificationType] = (
            [
                NotificationType(
                    id=f"event-{event.id}",
                    target=None if event.is_public else event.organization,
                    payload=event,
                    **{key: getattr(event, f"{key}_date") for key in ("start", "end")},
                )
                for event in Event.objects.filter(
                    **({"start_date__gte": start} if start is not None else {}),
                    **({"end_date__lte": start} if end is not None else {}),
                ).all()
            ]
            + [
                NotificationType(
                    id=f"announcement-{announcement.id}",
                    target=None
                    if announcement.is_public
                    else announcement.organization,
                    payload=announcement,
                    start=announcement.created_date,
                    end=announcement.last_modified_date,
                )
                for announcement in Announcement.objects.filter(
                    Q(is_public=True, tags__follower=info.context.user)
                    | Q(organization__member=info.context.user),
                    status="a",
                    **({"created_date__gte": start} if start is not None else {}),
                    **({"last_modified_date__lte": start} if end is not None else {}),
                ).all()
            ]
            + [
                NotificationType(
                    id=f"announcement-approval-{announcement.id}",
                    target=info.context.user,
                    payload=AnnouncementApprovalType(announcement=announcement),
                    start=announcement.created_date,
                    end=announcement.last_modified_date,
                )
                for announcement in Announcement.objects.filter(
                    status="p",
                    organization__supervisors__in=[info.context.user],
                    **({"created_date__gte": start} if start is not None else {}),
                    **({"last_modified_date__lte": start} if end is not None else {}),
                )
            ]
            + [
                NotificationType(
                    id=f"blogpost-{blogpost.id}",
                    target=None,
                    payload=blogpost,
                    start=blogpost.created_date,
                    end=blogpost.last_modified_date,
                )
                for blogpost in BlogPost.objects.filter(
                    is_published=True,
                    **({"created_date__gte": start} if start is not None else {}),
                    **({"last_modified_date__lte": start} if end is not None else {}),
                ).all()
            ]
        )
        return notifs
