import datetime
from functools import wraps
from typing import Literal

from django.core.cache import cache, caches
from django_redis.cache import RedisCache
from django.core.exceptions import PermissionDenied


def get_key_expiration(key: str, human_readable: bool = True):
    """
    Returns the number of seconds until the key expires.
    If the key does not expire, returns 0.
    If the key does not exist, returns 0.
    If human_readable is True, returns a string in the format Days HH:MM:SS (Days hours, minutes, seconds) or if it's Zero/Expired, returns "Now"
    """
    default_cache = caches["default"]

    if isinstance(default_cache, RedisCache):
        seconds_to_expiration = cache.ttl(key=key)
        if seconds_to_expiration is None:
            return 0 if not human_readable else "Now"
        return seconds_to_expiration
    else:
        # use make_key to generate Django's internal key storage name
        expiration_unix_timestamp = cache._expire_info.get(cache.make_key(key))
        if expiration_unix_timestamp is None:
            return 0 if not human_readable else "Now"
        expiration_date_time = datetime.datetime.fromtimestamp(
            expiration_unix_timestamp
        )

    now = datetime.datetime.now()

    # Be careful subtracting an older date from a newer date does not give zero
    if expiration_date_time < now:
        return 0 if not human_readable else "Now"
    # give me the seconds left till the key expires
    delta = expiration_date_time - now
    if human_readable:
        return "{:0>8}".format(str(datetime.timedelta(seconds=delta.seconds)))
    else:
        return delta.seconds


def admin_action_rate_limit(
    rate_limit: int =2,  # 2 actions per 10 minutes
    time_period: int =60 * 10,  # 10 minutes
    scope: Literal["user", "path"] = "path",
    must_be_staff: bool = True,
):
    def decorator(action_func):
        @wraps(action_func)
        def wrapper(modeladmin, request, queryset, *args, **kwargs):
            if must_be_staff and not request.user.is_staff:
                raise PermissionDenied(
                    "You must be a staff member to perform this action."
                )
            if scope == "user":
                key = f"admin_rate_limit_{request.user.pk}_{action_func.__name__}"
            else:
                key = f"admin_rate_limit_{request.user.pk}_{request.path}_{action_func.__name__}"  # shouldn't have to worry about key length as redis supports up to 512MB keys

            count = cache.get_or_set(key, 0, timeout=time_period)
            if count >= rate_limit:
                raise PermissionDenied(
                    f"Rate limit exceeded for this action, try again in {get_key_expiration(key)}"  # noqa
                )
            cache.incr(key)
            return action_func(modeladmin, request, queryset, *args, **kwargs)

        return wrapper

    return decorator
