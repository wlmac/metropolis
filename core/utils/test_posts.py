from django.test import TestCase
from django.utils import timezone

from core.admin import User
from core.models import Announcement, BlogPost, Organization


def create_school_org(user: User) -> Organization:
    school_org = Organization.objects.create(name="School Org")
    school_org.owners.set([user])
    school_org.save()
    return school_org


def create_user() -> User:
    user = User(username="bob")
    user.save()
    return user


def create_announcement(org: Organization, status: str, title: str) -> Announcement:
    ann = Announcement(
        organization=org, status=status, title=title, show_after=timezone.now()
    )
    ann.save()
    return ann


def create_blog_post(author: User, title: str) -> BlogPost:
    blog = BlogPost(
        author=author,
        is_published=True,
        title=title,
        show_after=timezone.now(),
    )
    blog.save()
    return blog


class TestAnnouncement(TestCase):
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
