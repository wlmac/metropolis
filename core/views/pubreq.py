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


class PubReqList(TemplateView, mixins.TitleMixin):
    template_name = "core/pubreq/list.html"
    title = "Requests for Publishing"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feed_all"] = models.PubReq.get_all(user=self.request.user)
        return context


class PubReqDetail(UserPassesTestMixin, DetailView, mixins.TitleMixin):
    model = models.PubReq
    context_object_name = "pubreq"
    template_name = "core/pubreq/detail.html"

    def test_func(self):
        pubreq = self.get_object()
        if self.request.user.is_superuser:
            return True
        if self.request.user == pubreq.organization.owner:
            return True
        if self.request.user in pubreq.organization.supervisors.all():
            return True
        if self.request.user in pubreq.organization.execs.all():
            return True
        if self.request.user in pubreq.requesters:
            return True
        if self.request.user in pubreq.approvers:
            return True
        return False

    def get_title(self):
        return self.get_object().title

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
