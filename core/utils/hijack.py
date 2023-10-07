import logging

import cachetools
from django.conf import settings

logger = logging.getLogger(__name__)
from hijack import signals


@cachetools.cached(cache=cachetools.LRUCache(maxsize=4096))
def hijack_permissions_check(*, hijacker, hijacked) -> bool:
    """Staff members may hijack other staff and regular users, but not superusers."""
    if all(
        [
            hijacker.id in settings.ALLOWED_HIJACKERS,
            hijacked.id not in settings.ALLOWED_HIJACKERS,
            hijacker.is_superuser,
            hijacked.is_active,
            not hijacked,
        ]
    ):
        return True
    return False


def print_hijack_started(sender, hijacker, hijacked, request, **kwargs):
    print(f"{hijacker} has hijacked {hijacked}")  # todo replace with logging


signals.hijack_started.connect(print_hijack_started)


def print_hijack_ended(sender, hijacker, hijacked, request, **kwargs):
    print(f"{hijacker} has released {hijacked}")


signals.hijack_ended.connect(print_hijack_ended)
