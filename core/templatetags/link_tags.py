from django import template
from django.shortcuts import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .. import models

register = template.Library()


@register.filter
def user_url(username):
    return reverse("profile_detail", args=[username])


@register.filter
def user(username, postfix=""):
    url = user_url(username)
    user_obj = models.User.objects.get(username=username)
    return format_html(
        '<a href="{0}{1}">{2}</a>',
        mark_safe(url),
        mark_safe(postfix),
        f"{user_obj.get_full_name()}",
    )


@register.filter
def users(usernames, postfix=""):
    users_string = ""
    for username in usernames:
        users_string += user(username, postfix) + ", "
    return users_string[:-2]


@register.filter
def timetable_url(timetable):
    return reverse("timetable_detail", args=[timetable])


@register.filter
def timetable(timetable, postfix=""):
    url = timetable_url(timetable)
    timetable_obj = models.Timetable.objects.get(pk=timetable)
    return format_html(
        '<a href="{0}{1}">{2}</a>',
        mark_safe(url),
        mark_safe(postfix),
        str(timetable_obj),
    )


@register.filter
def organization_url(organization):
    return reverse("organization_detail", args=[organization])


@register.filter
def organization(organization, postfix=""):
    url = organization_url(organization)
    organization_obj = models.Organization.objects.get(slug=organization)
    return format_html(
        '<a href="{0}{1}">{2}</a>',
        mark_safe(url),
        mark_safe(postfix),
        str(organization_obj),
    )


@register.filter
def announcement_url(announcement):
    return reverse("announcement_detail", args=[announcement])


@register.filter
def announcement(announcement, postfix=""):
    url = announcement_url(announcement)
    announcement_obj = models.Announcement.objects.get(pk=announcement)
    return format_html(
        '<a href="{0}{1}">{2}</a>',
        mark_safe(url),
        mark_safe(postfix),
        str(announcement_obj),
    )


@register.filter
def blogpost_url(blogpost):
    return reverse("blogpost_detail", args=[blogpost])


@register.filter
def blogpost(blogpost, postfix=""):
    url = blogpost_url(blogpost)
    blogpost_obj = models.BlogPost.objects.get(slug=blogpost)
    return format_html(
        '<a href="{0}{1}">{2}</a>',
        mark_safe(url),
        mark_safe(postfix),
        str(blogpost_obj),
    )
