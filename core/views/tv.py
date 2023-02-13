from django.views.generic import TemplateView

from . import mixins


class TVView(TemplateView, mixins.TitleMixin):
    template_name = "core/tv/index.html"
    title = "TV"


class TVClubView(TemplateView, mixins.TitleMixin):
    template_name = "core/tv/clubs.html"
    title = "Club Crawl"
