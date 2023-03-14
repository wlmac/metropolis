from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.models import BlogPost, Announcement


def likes(obj: "BlogPost" | "Announcement") -> int:
    likeCount = obj.likes.count()
    if likes is None:
        return 0
    return likeCount
