from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse
from functools import wraps


class TooManyRequests(HttpResponse):
    status_code = 429


def admin_action_rate_limit(
    view_func, rate_limit=2, time_period=60 * 10
):  # allow 2 action call of this type every 10 minutes
    @wraps(view_func)
    def _wrapped_view(modeladmin, request, queryset, *args, **kwargs):
        if request.user.is_staff and not request.user.is_superuser:
            key = f"admin_rate_limit_{request.user.pk}_{request.path}"
            count = cache.get_or_set(key, 0)

            if count >= rate_limit:
                return TooManyRequests(
                    "Rate limit exceeded for this action, try again later."
                )

            cache.incr(key)
            if (
                settings.CACHES["default"]["BACKEND"]
                != "django.core.cache.backends.locmem.LocMemCache"
            ):  # cache.expire doesn't work with LocMemCache
                cache.expire(key, time_period)

        return view_func(modeladmin, request, queryset, *args, **kwargs)

    return _wrapped_view
