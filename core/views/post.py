from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView
from django.views.generic.base import RedirectView, TemplateView

from .. import models
from . import mixins


class AnnouncementList(TemplateView, mixins.TitleMixin):
    template_name = "core/announcement/list.html"
    title = "Announcements"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["feed_all"] = models.Announcement.get_all(user=self.request.user)

        if self.request.user.is_authenticated:
            context["feed_my"] = self.request.user.get_feed()

        context["feeds_custom"] = []
        for custom_feed_organization_pk in settings.ANNOUNCEMENTS_CUSTOM_FEEDS:
            custom_feed_organization = models.Organization.objects.get(
                pk=custom_feed_organization_pk
            )
            context["feeds_custom"].append(
                (
                    custom_feed_organization,
                    custom_feed_organization.get_feed(user=self.request.user),
                )
            )

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
        if announcement.status == "a":
            if self.request.user in announcement.organization.members.all():
                return True
            if announcement.is_public:
                return True
        if self.request.user.is_superuser:
            return True
        if self.request.user == announcement.organization.owner:
            return True
        if self.request.user in announcement.organization.supervisors.all():
            return True
        if self.request.user in announcement.organization.execs.all():
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["feeds_custom"] = []
        for custom_feed_organization_pk in settings.ANNOUNCEMENTS_CUSTOM_FEEDS:
            custom_feed_organization = models.Organization.objects.get(
                pk=custom_feed_organization_pk
            )
            context["feeds_custom"].append(custom_feed_organization)

        return context


class BlogPostList(ListView, mixins.TitleMixin):
    context_object_name = "blogposts"
    template_name = "core/blogpost/list.html"
    title = "Blog Posts"

    def get_ordering(self):
        return "-last_modified_date"

    def get_queryset(self):
        return models.BlogPost.objects.filter(is_published=True)


class BlogPostDetail(UserPassesTestMixin, DetailView, mixins.TitleMixin):
    model = models.BlogPost
    context_object_name = "blogpost"
    template_name = "core/blogpost/detail.html"

    def get_title(self):
        return self.get_object().title

    def test_func(self):
        return self.get_object().is_published
