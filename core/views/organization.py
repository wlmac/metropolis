from django.db.models import Count
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, ListView
from django.views.generic.base import RedirectView

from .. import models
from . import mixins


class OrganizationList(ListView, mixins.TitleMixin):
    context_object_name = "organizations"
    template_name = "core/organization/list.html"
    title = "Clubs"

    def get_queryset(self):
        return (
            models.Organization.objects.filter(is_active=True)
            .annotate(num_member=Count("member"))
            .order_by("-num_member")
        )


class OrganizationDetail(DetailView, mixins.TitleMixin):
    model = models.Organization
    context_object_name = "organization"
    template_name = "core/organization/detail.html"

    def get_queryset(self):
        return models.Organization.objects.filter(is_active=True)

    def get_title(self):
        return self.get_object().name

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not self.get_object().is_open:
            return HttpResponseForbidden()
        if self.get_object() in request.user.organizations.all():
            request.user.organizations.remove(self.get_object())
        else:
            request.user.organizations.add(self.get_object())
        return redirect(self.get_object())


class OrganizationShort(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        org = get_object_or_404(models.Organization, pk=kwargs["pk"])
        return org.get_absolute_url()
