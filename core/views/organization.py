from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView
from django.views.generic.base import RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from .. import models
from . import mixins

class OrganizationList(ListView, mixins.TitleMixin):
    context_object_name = "organizations"
    template_name = 'core/organization/list.html'
    title = 'Clubs'
    model = models.Organization

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
