from django.shortcuts import redirect
from django.views.generic import DetailView, ListView

from . import mixins
from .. import models


class OrganizationList(ListView, mixins.TitleMixin):
    context_object_name = "organizations"
    template_name = 'core/organization/list.html'
    title = 'Clubs'
    model = models.Organization

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['organizations'] = sorted(models.Organization.objects.all(), key=lambda org: org.members.count())[::-1]
        return context

    def get_ordering(self):
        return "-name"


class OrganizationDetail(DetailView, mixins.TitleMixin):
    model = models.Organization
    context_object_name = "organization"
    template_name = "core/organization/detail.html"

    def get_title(self):
        return "Organization " + self.get_object().name

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not self.get_object().is_open:
            return HttpResponseForbidden()
        if self.get_object() in request.user.organizations.all():
            request.user.organizations.remove(self.get_object());
        else:
            request.user.organizations.add(self.get_object());
        return redirect(self.get_object());
