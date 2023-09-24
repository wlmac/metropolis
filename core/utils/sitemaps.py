from django.contrib.sitemaps import Sitemap, ping_google
from core.models import *
from metropolis.celery import app


class BlogSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.6

    def items(self):
        return BlogPost.public()

    @staticmethod
    def lastmod(obj):
        return obj.last_modified_date


class AnnouncementsSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        return Announcement.get_approved()

    @staticmethod
    def lastmod(obj):
        return obj.last_modified_date


class ClubsSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return Organization.active()


@receiver(post_save, sender=BlogPost)
@receiver(post_save, sender=Announcement)
@receiver(post_save, sender=Organization)
@app.task
def ping_sitemap_watchers(sender, instance, created, raw, update_fields, **kwargs):
    if settings.DEBUG:
        return
    if not created:
        return
    try:
        ping_google(sitemap_url="/sitemap.xml")
    except Exception:
        print("Could not ping Google.")
        # Bare 'except' because we could get a variety
        # of HTTP-related exceptions.
        pass
