"""
Copies public clubs, tags and announcements from the live site's API into the
local database so pages can be previewed with real data. Local dev only.

Usage:
    python manage.py pull_live [--site https://maclyonsden.com]

Images point at the live site's media if local_settings.py sets
MEDIA_URL = "https://maclyonsden.com/media/".
"""

import requests
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from core.models import Announcement, Organization, Tag


def media_path(url):
    return url.split("/media/", 1)[-1] if url else ""


class Command(BaseCommand):
    help = "Copy public clubs and announcements from the live API (DEBUG only)."

    def add_arguments(self, parser):
        parser.add_argument("--site", default="https://maclyonsden.com")

    def fetch(self, site, kind):
        url, rows = f"{site}/api/v3/obj/{kind}?limit=100", []
        while url:
            page = requests.get(url, timeout=30)
            page.raise_for_status()
            page = page.json()
            rows += page["results"]
            url = page["next"]
        return rows

    def handle(self, *args, site, **options):
        if not settings.DEBUG:
            raise CommandError("refusing to run with DEBUG off (is this prod?)")

        orgs = self.fetch(site, "organization")
        announcements = self.fetch(site, "announcement")

        tags = {t["id"]: t["name"] for row in orgs + announcements for t in row["tags"]}
        Tag.objects.bulk_create(
            [Tag(id=i, name=n) for i, n in tags.items()],
            update_conflicts=True,
            unique_fields=["id"],
            update_fields=["name"],
        )

        org_fields = ["name", "slug", "bio", "extra_content", "is_active"]
        Organization.objects.bulk_create(
            [
                Organization(
                    id=o["id"],
                    icon=media_path(o["icon"]),
                    banner=media_path(o["banner"]),
                    **{f: o[f] for f in org_fields},
                )
                for o in orgs
            ],
            update_conflicts=True,
            unique_fields=["id"],
            update_fields=[*org_fields, "icon", "banner"],
        )

        # the org list skips inactive clubs that old announcements still point at
        listed = {o["id"] for o in orgs}
        Organization.objects.bulk_create(
            [
                Organization(
                    id=o["id"],
                    name=o["name"],
                    slug=o["slug"],
                    icon=media_path(o["icon"]),
                    is_active=False,
                )
                for o in {
                    a["organization"]["id"]: a["organization"]
                    for a in announcements
                    if a["organization"] and a["organization"]["id"] not in listed
                }.values()
            ],
            ignore_conflicts=True,
        )

        ann_fields = ["title", "body", "show_after", "is_public", "status"]
        ann_fields += ["rejection_reason", "organization_string"]
        Announcement.objects.bulk_create(  # bulk_create skips post_save notifications
            [
                Announcement(
                    id=a["id"],
                    organization_id=(a["organization"] or {}).get("id"),
                    **{f: a[f] for f in ann_fields},
                )
                for a in announcements
            ],
            update_conflicts=True,
            unique_fields=["id"],
            update_fields=[*ann_fields, "organization"],
        )

        Through = Announcement.tags.through
        Through.objects.filter(
            announcement_id__in=[a["id"] for a in announcements]
        ).delete()
        Through.objects.bulk_create(
            [
                Through(announcement_id=a["id"], tag_id=t["id"])
                for a in announcements
                for t in a["tags"]
            ]
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"pulled {len(orgs)} clubs, {len(tags)} tags, {len(announcements)} announcements"
            )
        )
