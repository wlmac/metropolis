from django.views.generic.edit import CreateView, FormView
from django.views.generic import DetailView
from django.views import View
from .. import models
from . import mixins
from ..forms import AddTimetableSelectTermForm, AddTimetableSelectCoursesForm, AddCourseForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.http import JsonResponse

@method_decorator(login_required, name='dispatch')
class AddTimetableSelectTerm(FormView, mixins.TitleMixin):
    template_name = 'core/timetable/add/select_term.html'
    title = 'Add a Timetable'
    form_class = AddTimetableSelectTermForm

    def form_valid(self, form, **kwargs):
        return redirect('add_timetable_select_courses', pk=form.cleaned_data.get('term').pk)

    def get_form_kwargs(self):
        kwargs = super(FormView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class AddTimetableSelectCourses(LoginRequiredMixin, UserPassesTestMixin, CreateView, mixins.TitleMixin):
    template_name = 'core/timetable/add/select_courses.html'
    title = 'Add a Timetable'
    model = models.Timetable
    form_class = AddTimetableSelectCoursesForm

    def test_func(self):
        term = get_object_or_404(models.Term, pk=self.kwargs['pk'])
        try:
            models.Timetable.objects.get(owner=self.request.user, term=term)
        except models.Timetable.DoesNotExist:
            return True
        return False 

    def form_valid(self, form):
        model = form.save(commit=False)
        model.owner = self.request.user
        model.term = get_object_or_404(models.Term, pk=self.kwargs['pk'])
        model.save()

        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(CreateView, self).get_form_kwargs()
        kwargs['term'] = get_object_or_404(models.Term, pk=self.kwargs['pk'])
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['term'] = get_object_or_404(models.Term, pk=self.kwargs['pk'])
        return context

class AddCourse(LoginRequiredMixin, UserPassesTestMixin, CreateView, mixins.TitleMixin):
    template_name = 'core/course/add.html'
    title = 'Add a Course'
    model = models.Course
    form_class = AddCourseForm

    def test_func(self):
        term = get_object_or_404(models.Term, pk=self.kwargs['pk'])
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

class ViewTimetable(DetailView, mixins.TitleMixin):
    model = models.Timetable
    context_object_name = 'timetable'
    template_name = 'core/timetable/view.html'

    def get_title(self):
        return f'Timetable'

class ViewTimetableData(View):
    def get(self, request, pk):
        timetable = get_object_or_404(models.Timetable, pk=pk)
        return JsonResponse({'courses': [i.code for i in timetable.courses.all()]})
