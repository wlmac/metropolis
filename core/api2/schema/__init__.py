import graphene
from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned
from graphene_django import DjangoObjectType

from ... import utils
from ...models import Term
from . import course, notification, organization, post, tag, user, rfp


class Query(
    organization.Schema,
    course.Schema,
    post.Schema,
    tag.Schema,
    user.Schema,
    notification.Schema,
    graphene.ObjectType,
    rfp.Schema,
):
    version = graphene.String(
        description="The version of the API",
        required=True,
    )

    def resolve_version(self, info):
        return settings.API2_VERSION


schema = graphene.Schema(query=Query)
