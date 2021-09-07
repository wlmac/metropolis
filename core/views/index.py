from django.views.generic import DetailView, ListView
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.views import View
from .. import models
from . import mixins

class Index(TemplateView, mixins.TitleMixin):
    template_name = 'core/index.html'
    title = 'Dashboard'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # TODO: Refactor this later
        approved_announcements = models.Announcement.objects.filter(status='a')
        context['announcements'] = approved_announcements.filter(is_public=True)
        if self.request.user.is_authenticated:
            context['announcements'] |= approved_announcements.filter(organization__member=self.request.user)
        context['announcements'] = context['announcements'][:3]

        context['events'] = models.Event.objects.filter(is_public=True)
        if self.request.user.is_authenticated:
            context['events'] |= models.Event.objects.filter(organization__member=self.request.user)
        context['events'] = context['events'][:3]

        context['blogpost'] = models.BlogPost.objects.first()

        return context

class CalendarView(TemplateView):
    template_name = "core/calendar/view.html"

class Teapot(View):
    def get(self, request):
        return HttpResponse('orz teapot', status=418)
