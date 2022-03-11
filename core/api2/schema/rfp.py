from datetime import datetime
from typing import Optional

import graphene
from django.db.models import Q
from graphene_django import DjangoObjectType

from ...models import RfP
from .post import StatusType


class RfPType(DjangoObjectType):
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
        model = RfP


class Schema:
    rfps = graphene.List(
        RfPType,
        status=graphene.Argument(StatusType),
    )

    def resolve_rfps(
        self,
        info,
        status: Optional[StatusType] = None,
    ):
        return RfP.accessible_by(info.context.user).filter(
            **({"status": StatusType.db_status(status)} if status is not None else {}),
        ).distinct().all()
