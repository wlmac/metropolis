from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from core import models
from core.forms import (
    CourseFormSet,
    TimetableCreateOrUpdateForm,
)

from . import mixins


class TimetableList(LoginRequiredMixin, TemplateView, mixins.TitleMixin):
    template_name = "core/timetable/list.html"
    title = "Timetable"
    model = models.Timetable

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["timetable"] = self.request.user.get_timetable()
        return context


class TimetableEditor(LoginRequiredMixin, FormView, mixins.TitleMixin):
    template_name = "core/timetable/editor.html"
    title = "Timetable Editor"
    form_class = TimetableCreateOrUpdateForm
    success_url = reverse_lazy("timetable_list")

    def get_timetable(self):
        timetable, created = models.Timetable.objects.get_or_create(
            owner=self.request.user
        )

        if not hasattr(self, "created"):
            self.created = created

        return timetable

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        kwargs["instance"] = self.get_timetable()
        return kwargs

    def get_course_formset(self):
        timetable = self.get_timetable()

        if self.request.method == "POST":
            return CourseFormSet(self.request.POST, instance=timetable)

        # Force course forms to appear in order of period
        # regardless if it already exists
        existing_courses = timetable.courses.values_list("period", flat=True)
        for period in range(1, 5):
            if period not in existing_courses:
                models.Course.objects.create(timetable=timetable, period=period)

        return CourseFormSet(instance=timetable)

    def form_valid(self, form):
        timetable = form.save(commit=False)
        timetable.owner = self.request.user
        timetable.save()

        course_formset = self.get_course_formset()

        if not course_formset.is_valid():
            return self.render_to_response(
                self.get_context_data(
                    form=form, course_formset=self.get_course_formset()
                )
            )

        for period, course_form in enumerate(course_formset, 1):
            if not course_form.cleaned_data:
                continue

            course = course_form.save(commit=False)
            if course_form.is_empty():
                course.name = ""
                course.room = ""
                course.teacher = ""
                course.save()
            else:
                course.period = period
                course.save()

        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        context["timetable_created"] = self.created
        context["course_formset"] = self.get_course_formset()
        return context
