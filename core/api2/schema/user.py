from datetime import datetime
from typing import Optional

import graphene
from django.db.models import Q
from graphene_django import DjangoObjectType

from ...models import User


class UserType(DjangoObjectType):
    me = graphene.Boolean()

    def resolve_me(self, info):
        assert info.context.user.is_authenticated, "must be authenticated"
        return self.id == info.context.user.id

    class Meta:
        model = User
        exclude = (
            "is_staff",
            "password",
            "last_login",
            "email",
            "is_superuser",
            "is_active",
            "is_teacher",
            "announcements_approved",
            "course_set",
            "date_joined",
        )


class Schema:
    user = graphene.Field(UserType, username=graphene.String(required=True))
    me = graphene.Field(UserType)

    def resolve_user(self, info, username: str = None):
        return User.objects.filter(username=username).first()

    def resolve_me(self, info):
        assert info.context.user.is_authenticated
        return info.context.user
