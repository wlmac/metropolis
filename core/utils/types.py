from typing import TYPE_CHECKING, Final, Literal, NamedTuple

if TYPE_CHECKING:
    from core.api.v3.objects import BaseProvider

type APIObjOperations = Final[Literal["single", "new", "list", "retrieve"]]

type PathData = NamedTuple[str, "BaseProvider", dict]
