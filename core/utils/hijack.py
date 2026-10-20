import logging

from django.conf import settings
from hijack import signals

logger = logging.getLogger(__name__)


def hijack_permissions_check(*, hijacker, hijacked) -> bool:
    """
    ALLOWED_HIJACKERS may hijack any user, except another ALLOWED_HIJACKER
    You cannot hijack a non-active user as the db will not unlock.
    """
    return hijacked is not None and all(
        [
            hijacker.id in settings.ALLOWED_HIJACKERS,
            not hijacked.is_superuser,
            hijacker.is_superuser,
            hijacked.is_active,
        ]
    )


def print_hijack_started(sender, hijacker, hijacked, request, **kwargs):
    print(f"{hijacker} has hijacked {hijacked}")  # todo replace with logging


signals.hijack_started.connect(print_hijack_started)


def print_hijack_ended(sender, hijacker, hijacked, request, **kwargs):
    print(f"{hijacker} has released {hijacked}")


signals.hijack_ended.connect(print_hijack_ended)
