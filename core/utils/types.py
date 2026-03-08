from dataclasses import dataclass
from typing import TYPE_CHECKING, Final, Literal, NamedTuple, Optional

from rest_framework.serializers import BaseSerializer

if TYPE_CHECKING:
    from core.api.utils.polymorphism import ObjectAPIView
    from core.api.v3.objects import BaseProvider

type APIObjOperations = Final[Literal["single", "new", "list", "retrieve"]]

type PathData = NamedTuple[str, "BaseProvider", dict]


@dataclass
class SingleOperationData:
    providers: list["BaseProvider"]
    operation: APIObjOperations
    data: dict


@dataclass
class ProviderDetails:
    provider: "BaseProvider"
    operations_supported: dict[APIObjOperations, BaseSerializer]
    url: str | None = None
    view: Optional["ObjectAPIView"] = None

    def __hash__(self):
        return hash(self.provider.__class__.__name__)


@dataclass
class ObjectModificationData:
    retrieve: SingleOperationData | None = None
    single: SingleOperationData | None = None
    list: SingleOperationData | None = None
    new: SingleOperationData | None = None

    def __iter__(self):
        return iter(
            [
                ("retrieve", self.retrieve),
                ("single", self.single),
                ("list", self.list),
                ("new", self.new),
            ]
        )
