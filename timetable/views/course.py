from django.views.generic import DetailView
from django.views.generic.base import RedirectView
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .. import models
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
