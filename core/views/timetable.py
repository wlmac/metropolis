from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, FormMixin, FormView, UpdateView

from .. import models
from ..forms import (
    AddCourseForm,
    AddTimetableSelectTermForm,
    TimetableSelectCoursesForm,
)
from . import mixins


class TimetableList(LoginRequiredMixin, ListView, FormMixin, mixins.TitleMixin):
    template_name = "core/timetable/list.html"
    title = "Timetable"
    context_object_name = "timetables"
    model = models.Timetable
    form_class = AddTimetableSelectTermForm

    def get_queryset(self):
        return models.Timetable.objects.filter(owner=self.request.user)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, **kwargs):
        return redirect("timetable_create", pk=form.cleaned_data.get("term").pk)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class TimetableCreate(
    LoginRequiredMixin, UserPassesTestMixin, CreateView, mixins.TitleMixin
):
    template_name = "core/timetable/add.html"
    title = "Add a Timetable"
    model = models.Timetable
    form_class = TimetableSelectCoursesForm
    success_url = reverse_lazy("timetable_list")

    def test_func(self):
        term = get_object_or_404(models.Term, pk=self.kwargs["pk"])
        try:
            models.Timetable.objects.get(owner=self.request.user, term=term)
        except models.Timetable.DoesNotExist:
            return True
        return False

    def form_valid(self, form):
        model = form.save(commit=False)
        model.owner = self.request.user
        model.term = get_object_or_404(models.Term, pk=self.kwargs["pk"])
        model.save()

        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(CreateView, self).get_form_kwargs()
        kwargs["term"] = get_object_or_404(models.Term, pk=self.kwargs["pk"])
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["term"] = get_object_or_404(models.Term, pk=self.kwargs["pk"])
        return context


class TimetableUpdate(
    LoginRequiredMixin, UserPassesTestMixin, UpdateView, mixins.TitleMixin
):
    template_name = "core/timetable/edit.html"
    title = "Edit Timetable"
    model = models.Timetable
    form_class = TimetableSelectCoursesForm
    success_url = reverse_lazy("timetable_list")

    def test_func(self):
        return self.get_object().owner == self.request.user


class CourseCreate(
    LoginRequiredMixin, UserPassesTestMixin, CreateView, mixins.TitleMixin
):
    template_name = "core/course/add.html"
    title = "Add a Course"
    model = models.Course
    form_class = AddCourseForm

    def test_func(self):
        term = get_object_or_404(models.Term, pk=self.kwargs["pk"])
        return not term.is_frozen

    def form_valid(self, form):
        model = form.save(commit=False)
        model.term = get_object_or_404(models.Term, pk=self.kwargs["pk"])
        model.submitter = self.request.user
        model.save()

        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            return self.request.GET["next"]
        else:
            return reverse("timetable_list")

    def get_form_kwargs(self):
        kwargs = super(CreateView, self).get_form_kwargs()
        kwargs["term"] = get_object_or_404(models.Term, pk=self.kwargs["pk"])
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["term"] = get_object_or_404(models.Term, pk=self.kwargs["pk"])
        return context
