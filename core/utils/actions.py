import datetime as dt
import json
from functools import wraps

from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as __
from django.utils.translation import ngettext

from core.models import Announcement, Event, Organization, Post, User
from core.tasks import notif_events_singleday, notif_single
from core.utils.announcements import request_announcement_approval
from core.utils.ratelimiting import admin_action_rate_limit


def superuser_only(func):
    @wraps(func)
    def wrapper(modeladmin, request, queryset):
        if request.user.is_superuser:
            return func(modeladmin, request, queryset)
        else:
            raise PermissionDenied  # NOTE: for now, action is still visible to non-superusers

    return wrapper


# Events
@admin.action(
    permissions=["change"],
    description=__("Set the selected events to be hidden from public"),
)
def set_event_hidden(modeladmin, request, queryset: QuerySet[Event]):
    queryset.update(is_public=False)


@admin.action(
    permissions=["change"],
    description=__("Set the selected events to be visible to public"),
)
def set_event_visible(modeladmin, request, queryset: QuerySet[Event]):
    queryset.update(is_public=True)


@admin.action(permissions=["change"], description=__("Normalize Late Start events"))
def normalize_late_start(modeladmin, request, queryset: QuerySet[Event]):
    queryset = queryset.filter(name__icontains="late start")
    queryset.update(name="Late Start")


# Clubs
@admin.action(description=__("Set the selected clubs to inactive"))
@superuser_only
def set_club_unactive(modeladmin, request, queryset: QuerySet[Organization]):
    queryset.update(is_active=False)


@admin.action(description=__("Set the selected clubs to active"))
@superuser_only
def set_club_active(modeladmin, request, queryset: QuerySet[Organization]):
    queryset.update(is_active=True)


@admin.action(
    permissions=["change"],
    description=__("Set selected club's president to a temp user."),
)
@superuser_only
def reset_club_president(modeladmin, request, queryset: QuerySet[Organization]):
    for club in queryset:
        club.owners.set([User.objects.get(pk=970)])
        club.execs.set([User.objects.get(pk=970)])
        # 970 = temp user, not a real person.


@admin.action(
    permissions=["change"],
    description=__("Remove all club execs."),
)
def reset_club_execs(modeladmin, request, queryset: QuerySet[Organization]):
    for club in queryset:
        club.execs.clear()


@admin.action(
    permissions=["change"],
    description=__("Remove all club supervisors."),
)
@superuser_only
def reset_club_sups(modeladmin, request, queryset: QuerySet[Organization]):
    for club in queryset:
        club.supervisors.clear()


@admin.action(
    permissions=["change"],
    description=__("Replace club bios with placeholder text"),
)
@superuser_only
def wipe_club_bios(modeladmin, request, queryset: QuerySet[Organization]):
    queryset.update(bio="A WLMAC organization", extra_content="")


# Posts
@admin.action(
    permissions=["change"],
    description=__("Set the selected posts to archived (hidden from public)"),
)
def set_post_archived(modeladmin, request, queryset: QuerySet[Post]):
    queryset.update(is_archived=True)


@admin.action(
    permissions=["change"],
    description=__("Set the selected posts to unarchived (visible to public)"),
)
def set_post_unarchived(modeladmin, request, queryset: QuerySet[Post]):
    queryset.update(is_archived=False)


## Announcements


@admin.action(
    permissions=["view"],
    description=__("resend the approval email for the selected announcements"),
)
@admin_action_rate_limit(rate_limit=2, time_period=60 * 60)
def resend_approval_email(modeladmin, request, queryset: QuerySet[Announcement]):
    for post in queryset:
        request_announcement_approval(post)


# Users / Notifications
@admin.action(permissions=["change"], description=__("Send test notification"))
def send_test_notif(modeladmin, request, queryset):
    for u in queryset:
        notif_single.delay(
            u.id,
            dict(
                title="Test Notification",
                body="Test body.",
                category="test",
            ),
        )


@admin.action(permissions=["change"], description=__("Send singleday notification"))
def send_notif_singleday(modeladmin, request, queryset):
    for _ in queryset:
        notif_events_singleday.delay(date=dt.date.today())


@admin.action(
    permissions=["change"],
    description="Archive selected flatpages and download them as a JSON file",
)
def archive_page(modeladmin, request, queryset):
    if not request.user.has_perm("flatpages.change_flatpage"):
        raise RuntimeError("permissions kwarg doesn't work")

    response = HttpResponse(
        content_type="application/json"
    )  # write a json file with all the page date and then download it
    response["Content-Disposition"] = 'attachment; filename="pages.json"'
    data = []
    for page in queryset:
        data.append(
            {
                "url": page.url,
                "title": page.title,
                "content": page.content,
                "registration_required": page.registration_required,
                "template_name": page.template_name,
            }
        )
    response.write(json.dumps(data))
    return response


# Comments
@admin.action(
    permissions=["change"],
    description=__("Approve the selected comments for the main site."),
)
def approve_comments(self, request, queryset):
    count = queryset.update(live=True)
    self.message_user(
        request,
        ngettext(
            "%d comment successfully approved.",
            "%d comments successfully approved.",
            count,
        )
        % count,
    )


@admin.action(
    permissions=["change"],
    description=__("Unapprove the selected comments for the main site."),
)
def unapprove_comments(self, modeladmin, request, queryset):
    count = queryset.update(live=False)
    self.message_user(
        request,
        ngettext(
            "%d comment successfully unapproved.",
            "%d comments successfully unapproved.",
            count,
        )
        % count,
    )
