from django.views.generic import DetailView
from django.views.generic.base import RedirectView
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from .. import models
from ..forms import AddCourseForm
from . import mixins

@method_decorator(login_required, name='dispatch')
class SchoolRedirect(RedirectView):
    permanent = False
    query_string = False
    pattern_name = "view_school"

    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        return reverse(self.pattern_name, args=[user.school.pk])

class ViewSchool(DetailView, mixins.TitleMixin):
    model = models.School
    context_object_name = 'school'
    template_name = 'timetable/school/view.html'

    def get_title(self):
        return f'School {self.get_object().name}'

class ViewTerm(DetailView, mixins.TitleMixin):
    model = models.Term
    context_object_name = 'term'
    template_name = 'timetable/term/view.html'

    def get_title(self):
        return f'Term {self.get_object().name}'

class ViewCourse(DetailView, mixins.TitleMixin):
    model = models.Course
    context_object_name = 'course'
    template_name = 'timetable/course/view.html'

    def get_title(self):
        return f'Course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        context['users'] = [i.owner for i in models.Timetable.objects.filter(courses=course, term=course.term)]
        return context

class AddCourse(LoginRequiredMixin, UserPassesTestMixin, CreateView, mixins.TitleMixin):
    template_name = 'timetable/course/add.html'
    title = 'Add a Course'
    model = models.Course
    form_class = AddCourseForm

    def test_func(self):
        term = get_object_or_404(models.Term, pk=self.kwargs['pk'])
        if self.request.user.school != term.school:
            return False
        print(term.is_frozen)
        return not term.is_frozen

    def form_valid(self, form):
        model = form.save(commit=False)
        model.term = get_object_or_404(models.Term, pk=self.kwargs['pk'])
        model.save()

        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('add_timetable_select_courses', kwargs={'pk': self.kwargs['pk']})

    def get_form_kwargs(self):
        kwargs = super(CreateView, self).get_form_kwargs()
        kwargs['term'] = get_object_or_404(models.Term, pk=self.kwargs['pk'])
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['term'] = get_object_or_404(models.Term, pk=self.kwargs['pk'])
        return context
