"""
This script is used to add organizations from a Google Sheets link. It is used to add organizations that are not already in the database.
Code owned by Phil of metropolis backend team.

Usage:
    python manage.py add_clubs <google_sheets_link>
"""

from __future__ import annotations

import csv
from io import StringIO
import re

import requests
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.db.models import Q

from core.models import Organization, User


class Command(BaseCommand):
    help = "Adds organizations from Google Sheets. Does not modify existing organizations. See https://github.com/wlmac/metropolis/issues/247"

    def error(self, *args, **kwargs):
        self.stdout.write(
            self.style.ERROR(*args, **kwargs),
        )

    def success(self, *args, **kwargs):
        self.stdout.write(
            self.style.SUCCESS(*args, **kwargs),
        )

    def warn(self, *args, **kwargs):
        self.stdout.write(
            self.style.WARNING(*args, **kwargs),
        )

    def add_arguments(self, parser):
        parser.add_argument(
            "sheets_link",
            type=str,
            help="Link to Google Sheets (must be published as CSV). "
            "Follow this guide (https://support.google.com/docs/answer/183965) to publish the spreadsheet, "
            "set the dropbox to 'Comma-separated-values (.csv)' and copy the link underneath (https://web.archive.org/web/20240902165418/https://cdn.discordapp.com/attachments/1280208592712241285/1280209073949638717/publish_to_web.png?ex=66d73f1c&is=66d5ed9c&hm=616b70187f8f3a54885b050e5f80c606d275318382333e5819364e020ba421bb&)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Don't actually add the organizations to the database",
        )

    def handle(self, *args, **options):
        sheets_url = str(options["sheets_link"])
        if not ("output=csv" in sheets_url or sheets_url.endswith(".csv")):
            raise AssertionError(
                "Make sure to make a copy of the club spreadsheet and use the link provided when publishing as .csv file (https://support.google.com/docs/answer/183965)"
            )

        csv_reader = csv.reader(StringIO(requests.get(sheets_url).text))

        expected_header = [
            "Timestamp",
            "Email Address",
            "Club/Council Name",
            "President(s) - include grade",
            "All Paid Activity Fee?",
            "President(s) Email",
            "Confirmation that all club/council executives have paid the mandatory student registration fee.",
            "Staff Supervisor(s)",
            "Staff Supervisor(s) Email",
            "Description of Club/Council",
            "Time + Place of Club/Council Meetings",
            "Major Initiatives/Events",
            "Social Media Links/Usernames",
            "Approximate Budget Requested (include allocation + reasoning)",
            "Declaration that this prospective club/council is willing to participate in Student Council Events.",
            "President's Username",
            "Supervisor's Username",
        ]

        header = next(csv_reader)

        assert expected_header == header, (
            "Google Sheets layout changed since the last time the script was updated, please consult the backend team."
        )

        skipped_data = []
        for row in csv_reader:
            row = [token.strip() for token in row]
            (
                _,
                submitter_email,
                organization_name,
                _,
                saf_paid,
                owner_emails,
                _,
                _,
                staff_emails,
                description,
                time_and_place,
                _,
                social_links,
                _,
                _,
                owner_usernames,
                staff_usernames,
            ) = row

            if len(organization_name) == 0 or saf_paid != "YES":
                self.warn(
                    f"Skipping {organization_name} as it is either not a club or has not paid the SAF."
                )
                continue

            self.success(f"\nNew organization: {organization_name}")

            owner_emails = self.extract_emails(owner_emails)
            staff_emails = self.extract_emails(staff_emails)

            owner_users = []
            supervisor_users = []

            for owner_email in owner_emails:
                user = self.get_user_by_email(owner_email, owner_usernames)
                if user == "skipped":
                    skipped_data.append(
                        f"President user `{owner_email}` not found in club `{organization_name}`"
                    )
                    continue
                owner_users.append(user)

            for staff_email in staff_emails:
                user = self.get_user_by_email(staff_email, staff_usernames)
                if user == "skipped":
                    skipped_data.append(
                        f"Supervisor user `{staff_email}` not found in club `{organization_name}`"
                    )
                    continue
                supervisor_users.append(user)

            skip = False

            if len(owner_users) == 0:
                self.error(
                    f"Skipping `{organization_name}` as there are no owners with emails `{owner_emails}`"
                )
                skipped_data.append(
                    f"Skipped `{organization_name}` as there are no owners with emails `{owner_emails}`"
                )
                skip = True

            if len(supervisor_users) == 0:
                skipped_data.append(
                    f"`{organization_name}` has no staff supervisor accounts with emails `{staff_emails}`"
                )

            if skip:
                continue

            try:
                defaults = {
                    "owners": owner_users,
                    "name": organization_name,
                    "extra_content": description + "\n\n" + time_and_place,
                    "show_members": True,
                    "is_active": True,
                    "is_open": False,
                    "applications_open": False,
                }

                possible_slugs = self.get_slugs_from_name(organization_name)

                slug = next(
                    (
                        Organization.objects.filter(slug=slug).first().slug
                        for slug in set(possible_slugs)
                        if Organization.objects.filter(slug=slug).exists()
                    ),
                    None,
                )

                slug = slug or self.get_corrected_slug_or_not(
                    possible_slugs, organization_name
                )

                if not options["dry_run"]:
                    club, created = Organization.objects.update_or_create(
                        slug=slug,
                        defaults=defaults,
                        create_defaults={
                            **defaults,
                            "bio": "A WLMAC organization",
                        },
                    )
                    club.execs.add(owner_users)
                    club.supervisors.add(supervisor_users)

                    status = "added" if created else "updated"
                else:
                    status = "(dry-run | would have added)"
                self.success(
                    f"\tSuccessfully {status} '{organization_name}' organization (slug={slug}), owned by {owner_users}, supervised by {supervisor_users}"
                )
            except IntegrityError as IE:
                self.error(IE.__traceback__)
            self.stdout.write()

        self.warn(f"Job finished with {len(skipped_data)} warnings:")
        for warning in skipped_data:
            self.warn(warning)
        self.success("Done!")

    type Status = "skipped"  # noqa: F821

    def extract_emails(self, emails: str) -> list[str]:
        email_pattern = r"\S+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
        return re.findall(email_pattern, emails)

    def get_slugs_from_name(self, organization_name: str) -> list[str]:
        # set to lowercase, remove all non-alphanumeric or whitespace characters (a-z 0-9, space) and then replace spaces with dashes
        slugs = []
        slug_lower = organization_name.strip().casefold()
        slug = re.sub(r"[^a-zA-Z0-9\s]", "", slug_lower).replace(" ", "-")
        slugs.append(slug)

        # without "club" in name
        slug = slug_lower.replace("club", "").replace("  ", " ").strip()
        slug = re.sub(r"[^a-zA-Z0-9\s]", "", slug).replace(" ", "-")
        slugs.append(slug)

        return slugs

    def get_user_by_email(self, email: str, fallback_data: str) -> User | Status:
        try:
            user = User.objects.get(email__iexact=email)
            self.success(f"\tUser with email ({email}) found!")
            return user
        except User.DoesNotExist:
            self.error(
                f"\tEmail ({email}) not found! Are you sure they registered a metro account with this email?"
            )
            self.stdout.write(f"\tData: {fallback_data}")

            self.stdout.write(
                "\tIf you have the correct email OR username, please enter it here (type 'skip' to skip this entry):"
            )
            while True:
                try:
                    print("\t", end="")
                    inp = input().casefold()
                    if len(inp) == 0 or inp == "skip":
                        return "skipped"
                    return User.objects.get(
                        Q(email__iexact=inp) | Q(username__iexact=inp)
                    )
                except User.DoesNotExist:
                    self.error(
                        "\tUser not found. Did you make a typo? (type 'skip' to skip this user)"
                    )

                    self.stdout.write("\tPlease re-enter email:")

    def get_corrected_slug_or_not(
        self, possible_slugs: list[str], organization_name: str
    ) -> str:
        self.warn(
            f"\tCould not find '{organization_name}' with the any of the slugs: {set(possible_slugs)}. "
        )

        self.stdout.write(
            f"\tPlease enter the correct slug if the organization exists or leave blank to create club with slug {possible_slugs[0]}:"
        )

        while True:
            print("\t", end="")
            new_slug = input()

            if new_slug == "":
                return possible_slugs[0]
            elif Organization.objects.filter(slug=new_slug).exists():
                return new_slug
            else:
                self.error(
                    f"\tCould not find an organization with the slug '{new_slug}'. Please try again or leave blank to create a club."
                )
