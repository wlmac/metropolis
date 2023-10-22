import datetime as dt
import json

from django.conf import settings
from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext_lazy as _, ngettext

from core.models import Post, User, Organization, Announcement
from core.tasks import notif_single, notif_events_singleday
from core.utils.mail import send_mail
from core.utils.ratelimiting import admin_action_rate_limit


# Clubs
@admin.action(
    permissions=["change"], description=_("Set the selected clubs to unactive")
)
def set_club_unactive(modeladmin, request, queryset: QuerySet[Organization]):
    queryset.update(is_active=False)


@admin.action(permissions=["change"], description=_("Set the selected clubs to active"))
def set_club_active(modeladmin, request, queryset: QuerySet[Organization]):
    queryset.update(is_active=True)


@admin.action(
    permissions=["change"],
    description=_("Set selected club's president to a temp user."),
)
def reset_club_president(modeladmin, request, queryset: QuerySet[Organization]):
    queryset.update(owner=User.objects.get(id=970))  # temp user, not a real person.


@admin.action(
    permissions=["change"],
    description=_("Remove all club execs."),
)
def reset_club_execs(modeladmin, request, queryset: QuerySet[Organization]):
    for club in queryset:
        club.execs.clear()


# Posts
@admin.action(
    permissions=["change"],
    description=_("Set the selected posts to archived (hidden from public)"),
)
def set_post_archived(modeladmin, request, queryset: QuerySet[Post]):
    queryset.update(is_archived=True)


@admin.action(
    permissions=["change"],
    description=_("Set the selected posts to unarchived (visible to public)"),
)
def set_post_unarchived(modeladmin, request, queryset: QuerySet[Post]):
    queryset.update(is_archived=False)


## Announcements


@admin.action(
    permissions=["view"],
    description=_("resend the approval email for the selected announcements"),
)
@admin_action_rate_limit
def resend_approval_email(modeladmin, request, queryset: QuerySet[Announcement]):
    for post in queryset:
        for teacher in post.organization.supervisors.all():
            email_template_context = {
                "teacher": teacher,
                "announcement": post,
                "review_link": settings.SITE_URL
                + reverse("admin:core_announcement_change", args=(post.pk,)),
            }

            send_mail(
                f"[ACTION REQUIRED] An announcement for {post.organization.name} needs your approval.",
                render_to_string(
                    "core/email/verify_announcement.txt",
                    email_template_context,
                ),
                None,
                [teacher.email],
                bcc=settings.ANNOUNCEMENT_APPROVAL_BCC_LIST,
                html_message=render_to_string(
                    "core/email/verify_announcement.html",
                    email_template_context,
                ),
            )


# Users / Notifications
@admin.action(permissions=["change"], description=_("Send test notification"))
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


@admin.action(permissions=["change"], description=_("Send singleday notification"))
def send_notif_singleday(modeladmin, request, queryset):
    for _ in queryset:
        notif_events_singleday.delay(date=dt.date.today())


# FlatPages


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
    description=_("Approve the selected comments for the main site."),
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
    description=_("Unapprove the selected comments for the main site."),
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
