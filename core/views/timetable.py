from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from core import models
from core.forms import (
    TimetableCreateOrUpdateForm,
)

from . import mixins


class TimetableList(LoginRequiredMixin, TemplateView, mixins.TitleMixin):
    template_name = "core/timetable/list.html"
    title = "Timetable"
    model = models.Timetable

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["timetable"] = getattr(self.request.user, "timetable", None)
        return context


class TimetableEditor(LoginRequiredMixin, FormView, mixins.TitleMixin):
    template_name = "core/timetable/editor.html"
    title = "Timetable Editor"
    form_class = TimetableCreateOrUpdateForm
    success_url = reverse_lazy("timetable_list")

    def get_object(self):
        obj = getattr(self.request.user, "timetable", None)
        return obj

    def form_valid(self, form):
        timetable = form.save(commit=False)
        timetable.owner = self.request.user
        timetable.save()

        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        instance = self.get_object()
        if instance:
            kwargs["instance"] = instance
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_edit"] = self.get_object() is not None
        return context
