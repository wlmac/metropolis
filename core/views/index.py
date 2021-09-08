from django.views.generic import DetailView, ListView
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.views import View
from .. import models
from . import mixins

class Index(TemplateView, mixins.TitleMixin):
    template_name = 'core/index.html'
    title = 'Dashboard'

class CalendarView(TemplateView):
    template_name = "core/calendar/view.html"

class Teapot(View):
    def get(self, request):
        return HttpResponse('orz teapot', status=418)
