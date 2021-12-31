from datetime import datetime
from typing import Optional

import graphene
from django.db.models import Q
from graphene_django import DjangoObjectType

from ...models import Tag


class TagType(DjangoObjectType):
    is_following = graphene.Boolean()
    color = graphene.String(
        description="Color of the tag in HTML " "format (e.g. #ff0000 for red)"
    )

    def resolve_is_following(self, info):
        assert (
            info.context.user.is_authenticated
        ), "User must be authenticated to follow a tag"
        return info.context.user.tags_following.filter(id=self.id).exists()

    def resolve_color(self, info):
        return self.color()

    class Meta:
        model = Tag


class Schema:
    following_tags = graphene.List(TagType)
    tags = graphene.List(TagType)

    def resolve_following_tags(self, info):
        assert (
            info.context.user.is_authenticated
        ), "User must be authenticated to get the tags it follows"
        return info.context.user.tags_following.all()

    def resolve_tags(self, info):
        return Tag.objects.all()
