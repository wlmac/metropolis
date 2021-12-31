from typing import Optional

import graphene
from django.db.models import Q
from graphene_django import DjangoObjectType

from ...models import Organization, OrganizationURL
from .post import AnnouncementType


class OrganizationType(DjangoObjectType):
    absolute_url = graphene.String()
    member_count = graphene.Int()
    feed = graphene.List(AnnouncementType)
    is_member = graphene.Boolean()
    me = graphene.Boolean()

    def resolve_absolute_url(self, info):
        return self.get_absolute_url()

    def resolve_member_count(self, info):
        return self.member_count()

    def resolve_feed(self, info):
        return self.get_feed(user=info.context.user)

    def resolve_is_member(self, info):
        return Organization.objects.filter(member__in=[info.context.user]).exists()

    def resolve_me(self, info):
        return Organization.objects.filter(
            Q(member__in=[info.context.user])
            | Q(execs__in=[info.context.user])
            | Q(supervisors__in=[info.context.user])
            | Q(owner=info.context.user)
        ).exists()

    class Meta:
        model = Organization


class Schema:
    organizations = graphene.List(OrganizationType, is_member=graphene.Boolean())

    def resolve_organizations(self, info, is_member: Optional[bool] = None):
        if not info.context.user.is_authenticated and is_member is not None:
            raise Exception("You must be logged in to filter by membership status.")
        return Organization.objects.filter(
            **({"member__in": [info.context.user]} if is_member is not None else {}),
        ).all()
