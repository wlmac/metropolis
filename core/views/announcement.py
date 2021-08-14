from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.db.models import Q
from .. import models
from . import mixins
from metropolis import settings

class AnnouncementList(TemplateView, mixins.TitleMixin):
    template_name = 'core/announcement/list.html'
    title = 'Announcements'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        approved_announcements = models.Announcement.objects.filter(is_approved=True)
        context['feed_all'] = approved_announcements.filter(Q(is_public=True) | Q(organization__member=self.request.user))
        context['feed_my'] = approved_announcements.filter(Q(is_public=True, tags__follower=self.request.user) | Q(organization__member=self.request.user)).distinct()

        context['feeds_custom'] = []
        for custom_feed_organization_slug in settings.NEWS_CUSTOM_FEEDS:
            custom_feed_organization = models.Organization.objects.get(slug=custom_feed_organization_slug)
            custom_feed_queryset = approved_announcements.filter(organization__slug=custom_feed_organization_slug)
            if self.request.user not in custom_feed_organization.members.all():
                custom_feed_queryset = custom_feed_queryset.filter(is_public=True)
            context['feeds_custom'].append((custom_feed_organization, custom_feed_queryset))

        return context
