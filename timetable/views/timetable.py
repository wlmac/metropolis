from django.views.generic.edit import CreateView
from django.views.generic import DetailView
from .. import models
from . import mixins
from ..forms import AddTimetableForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@method_decorator(login_required, name='dispatch')
class AddTimetable(CreateView, mixins.TitleMixin):
    template_name = 'timetable/timetable/add.html'
    title = 'Add a Timetable'
    model = models.Timetable
    form_class = AddTimetableForm

    def form_valid(self, form, **kwargs):
        model = form.save(commit=False)
        model.owner = self.request.user
        model.save()

        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(CreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class ViewTimetable(DetailView, mixins.TitleMixin):
    model = models.Timetable
    context_object_name = 'timetable'
    template_name = 'timetable/timetable/view.html'

    def get_title(self):
        return f'Timetable'
