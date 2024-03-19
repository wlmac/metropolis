from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, Final, List, Literal, NamedTuple, Optional

from rest_framework.serializers import BaseSerializer

from typing import TYPE_CHECKING, Final, Literal, NamedTuple


if TYPE_CHECKING:
    from core.api.utils.polymorphism import ObjectAPIView
    from core.api.v3.objects import BaseProvider

type APIObjOperations = Final[Literal["single", "new", "list", "retrieve"]]

type PathData = NamedTuple[str, "BaseProvider", dict]


@dataclass
class SingleOperationData:
    providers: List["BaseProvider"]
    operation: APIObjOperations
    data: dict


@dataclass
class ProviderDetails:
    provider: "BaseProvider"
    operations_supported: Dict[APIObjOperations, BaseSerializer]
    url: Optional[str] = None
    view: Optional["ObjectAPIView"] = None

    def __hash__(self):
        return hash(self.provider.__class__.__name__)


@dataclass
class ObjectModificationData:
    retrieve: Optional[SingleOperationData] = None
    single: Optional[SingleOperationData] = None
    list: Optional[SingleOperationData] = None
    new: Optional[SingleOperationData] = None

    def __iter__(self):
        return iter(
            [
                ("retrieve", self.retrieve),
                ("single", self.single),
                ("list", self.list),
                ("new", self.new),
            ]
        )
