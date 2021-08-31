from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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
        approved_announcements = models.Announcement.objects.filter(status='a')
        context['feed_all'] = approved_announcements.filter(is_public=True)
        if self.request.user.is_authenticated:
            context['feed_all'] |= approved_announcements.filter(organization__member=self.request.user)
            context['feed_my'] = approved_announcements.filter(Q(is_public=True, tags__follower=self.request.user) | Q(organization__member=self.request.user)).distinct()

        context['feeds_custom'] = []
        for custom_feed_organization_pk in settings.ANNOUNCEMENTS_CUSTOM_FEEDS:
            custom_feed_organization = models.Organization.objects.get(pk=custom_feed_organization_pk)
            custom_feed_queryset = approved_announcements.filter(organization__pk=custom_feed_organization_pk)
            if self.request.user not in custom_feed_organization.members.all():
                custom_feed_queryset = custom_feed_queryset.filter(is_public=True)
            context['feeds_custom'].append((custom_feed_organization, custom_feed_queryset))

        """ to-do: search bar, DNR
        query = self.request.GET.get('q' ,'')
        feed_type = self.request.GET.get('ft','')
        print(feed_type)
        if query != '':
            if feed_type == 'get':
                context['search'] = context['feed_all'].filter(pk=query)
            else:
                context['search'] = context['feed_all'].filter(Q(body__icontains=query) | Q(title__icontains=query))
        """
        return context

class AnnouncementDetail(UserPassesTestMixin, DetailView, mixins.TitleMixin):
    model = models.Announcement
    context_object_name = "announcement"
    template_name = "core/announcement/detail.html"

    def get_title(self):
        return self.get_object().title

    def test_func(self):
        announcement = self.get_object()
        return announcement.status == 'a' and (announcement.is_public or self.request.user in announcement.organization.members.all())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['feeds_custom'] = []
        for custom_feed_organization_pk in settings.ANNOUNCEMENTS_CUSTOM_FEEDS:
            custom_feed_organization = models.Organization.objects.get(pk=custom_feed_organization_pk)
            context['feeds_custom'].append(custom_feed_organization)
        
        return context
