from django.views.generic import DetailView, ListView
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.views import View
from metropolis import settings
from .. import models
from . import mixins

class Index(TemplateView, mixins.TitleMixin):
    template_name = 'core/index.html'
    title = 'Dashboard'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['announcements'] = models.Announcement.get_all(user=self.request.user)[:3]

        context['events'] = models.Event.objects.filter(is_public=True)
        if self.request.user.is_authenticated:
            context['events'] = (context['events'] | models.Event.objects.filter(organization__member=self.request.user)).distinct()
        context['events'] = context['events'][:3]

        context['blogpost'] = models.BlogPost.objects.first()

        return context

class CalendarView(TemplateView, mixins.TitleMixin):
    template_name = "core/calendar/view.html"
    title = 'Calendar'

class MapView(TemplateView, mixins.TitleMixin):
    template_name = "core/map/map.html"
    title = 'Map'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mapbox_apikey'] = {'apikey': settings.MAPBOX_APIKEY}
        return context

class Teapot(View):
    def get(self, request):
        return HttpResponse('orz teapot', status=418)
