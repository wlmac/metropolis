from django.conf import settings
from django.db.models import Count
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView, TemplateView

from .. import models
from . import mixins


class TVView(TemplateView, mixins.TitleMixin):
    template_name = "core/tv/index.html"
    title = "TV"


class TVClubView(TemplateView, mixins.TitleMixin):
    template_name = "core/tv/clubs.html"
    title = "Club Crawl"
