import csv
import numpy as np
import requests

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from core.models import User, Organization
from io import StringIO


class Command(BaseCommand):
    help = "Adds organizations from Google Sheets. Does not modify existing organizations. See https://github.com/wlmac/metropolis/issues/247"

    def add_arguments(self, parser):
        parser.add_argument('sheets_link', type=str, help='Link to Google Sheets (must be published as CSV)')

    def handle(self, *args, **options):
        assert "?output=csv" in options['sheets_link'], \
            "Make sure make a copy of the club spreadsheet and use the link provided when publishing as CSV (https://support.google.com/docs/answer/183965)"
        
        csv_reader = csv.reader(
                        StringIO(
                            requests.get( options['sheets_link'] ).text
                        )
                    )

        expected_header = [
                    "CLUB NAME",
                    "APPROVED & MAILED",
                    "SAF PAID",
                    "PRESIDENT(S)",
                    "PRESIDENT(S) EMAIL",
                    "STAFF SUPERVISOR(S)",
                    "STAFF(S) EMAIL",
                    "BUDGET REQUEST",
                    "TIME + PLACE",
                    "SOCIAL LINKS"
                 ]

        assert expected_header == next(csv_reader), \
            "Google Sheets layout changed since the last time the script was updated"

        for row in csv_reader:
            organization_is_not_approved = row[1]!='TRUE'
            has_duplicate_owner = len(row[0]) == 0
            if organization_is_not_approved or has_duplicate_owner:
                continue
            
            self.stdout.write(f"New organization: {row[0]}")
            organization_name, _, _, owner_name, owner_email, _, _, _, time_and_place, social_links = row

            owner_user = None
            try:
                owner_user = User.objects.get(email=owner_email)
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(
                        f"\t{owner_name}'s email not found! Are you sure they registered a metro account with this email?"
                    )
                )

                skip_entry = False
                self.stdout.write("\tIf you have the correct email, please enter it here:")
                while True:
                    try:
                        print("\t", end="")
                        owner_email = input()
                        owner_user = User.objects.get(email=owner_email)
                        break
                    except User.DoesNotExist:
                        if len(owner_email) == 0:
                            skip_entry = True
                            break

                        self.stdout.write(self.style.ERROR("\tUser not found. Did you make a typo?"))
                        self.stdout.write("\tPlease re-enter email:")

                if skip_entry == True:
                    self.stdout.write(f"\tSkipped creation of {organization_name}")
                    continue
            self.stdout.write(self.style.SUCCESS(f"\tFound a match for {owner_name}'s email"))

            try:
                # Consider using get_or_create() if it happens to be more useful?
                # Also, consider updating the google sheets table so we can automatically fill out bio and slug and stuff
                club = Organization(
                    owner=owner_user,
                    name=organization_name,
                    bio="A WLMAC organization",
                    extra_content=time_and_place + "\n\n" + social_links,
                    slug='' # very crude ik
                        .join(c if c.isalnum() else '-' for c in organization_name)
                        .lower(),
                    show_members=True,
                    is_active=True,
                    is_open=False,
                )
                club.save()
                club.execs.add(owner_user)

                self.stdout.write(
                    self.style.SUCCESS(f"\tSuccessfully added {organization_name} organization, owned by {owner_name}")
                )
            except IntegrityError:
                self.stdout.write(
                    self.style.ERROR("\tDuplicate slug detected. Skipping...")
                )
            self.stdout.write()
