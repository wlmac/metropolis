from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from core import models


class PostTypeFilter(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _("Post Type")

    # Parameter for the filter that will be used in the URL query.
    parameter_name = "post_type"

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return [
            (16, _("An announcement")),
            (18, _("A Blog Post")),
            (32, _("An Exhibit")),
        ]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() is None:
            return queryset
        return queryset.filter(content_type=self.value())


class OrganizationListFilter(admin.SimpleListFilter):
    title = "organization"
    parameter_name = "org"

    def lookups(self, request, model_admin):
        qs = models.Organization.objects.all()
        if not request.user.is_superuser:
            qs = qs.filter(
                Q(owner=request.user)
                | Q(supervisors=request.user)
                | Q(execs=request.user)
            ).distinct()
        for org in qs:
            yield (org.slug, org.name)

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        else:
            return queryset.filter(organization__slug=self.value())


class BlogPostAuthorListFilter(admin.SimpleListFilter):
    title = "author"
    parameter_name = "author"

    def lookups(self, request, model_admin):
        qs = models.User.objects.filter(blogposts_authored__isnull=False).distinct()
        for author in qs:
            yield (author.pk, author.username)

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        else:
            return queryset.filter(author__pk=self.value())
