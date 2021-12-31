from datetime import datetime
from typing import Optional

import graphene
from graphene_django import DjangoObjectType

from ...models import Course, Event, Term


class TermType(DjangoObjectType):
    is_current = graphene.Boolean()

    def resolve_is_current(self, info):
        return self.is_current()

    class Meta:
        model = Term


class CourseType(DjangoObjectType):
    class Meta:
        model = Course


class EventType(DjangoObjectType):
    class Meta:
        model = Event


class Schema:
    terms = graphene.List(TermType)
    current_term = graphene.Field(TermType)
    courses = graphene.List(CourseType)
    events = graphene.List(
        EventType,
        start=graphene.DateTime(required=True),
        end=graphene.DateTime(),
        is_public=graphene.Boolean(),
        by_member_organizations=graphene.Boolean(),
    )

    def resolve_terms(self, info):
        return Term.objects.all()

    def resolve_is_current(self, info):
        return Term.get_current()

    def resolve_courses(self, info):
        return Course.objects.all()

    def resolve_events(
        self,
        info,
        start: datetime,
        end: Optional[datetime] = None,
        is_public: Optional[bool] = None,
        by_member_organizations: Optional[bool] = None,
    ):
        if not info.context.user.is_authenticated and by_member_organizations == True:
            raise TypeError("You must be logged in to query by member organizations")
        return Event.objects.filter(
            end_date__gte=start,
            **({"start_date__lte": end} if end is not None else {}),
            **({"is_public": is_public} if is_public is not None else {}),
            **(
                {"organization__member": info.context.user.id}
                if by_member_organizations is not None
                else {}
            ),
        ).all()
