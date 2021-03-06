from django.test import TestCase

from . import Organization, User
from .post import *


def create_school_org(user: User) -> Organization:
    school_org = Organization(owner=user)
    school_org.save()
    return school_org


def create_user() -> User:
    user = User(username="bob")
    user.save()
    return user


def create_announcement(org: Organization, status: str, title: str) -> Announcement:
    ann = Announcement(organization=org, status=status, title=title)
    ann.save()


class AnnouncementTests(TestCase):
    def test_get_approved(self):
        org = create_school_org(create_user())
        create_announcement(org, "p", "hello")
        create_announcement(org, "p", "goodbye")
        create_announcement(org, "a", "foo")
        create_announcement(org, "a", "abc")
        create_announcement(org, "a", "bar")
        create_announcement(org, "r", "bad")
        create_announcement(org, "r", "good")
        approved = sorted(ann.title for ann in Announcement.get_approved())
        self.assertEqual(approved, ["abc", "bar", "foo"])
