from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView

from core.utils import generate_slam as gs

from .. import models
from . import mixins


class Index(TemplateView, mixins.TitleMixin):
    template_name = "core/index.html"
    title = "Home"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["announcements"] = models.Announcement.get_all(user=self.request.user)[
            :3
        ]

        datetime_now = timezone.localtime()
        context["events"] = models.Event.get_events(user=self.request.user).filter(
            start_date__lte=datetime_now, end_date__gte=datetime_now
        )[:3]

        context["blogpost"] = models.BlogPost.objects.filter(is_published=True).first()

        return context


class CalendarView(TemplateView, mixins.TitleMixin):
    template_name = "core/calendar/view.html"
    title = "Calendar"


class MapView(TemplateView, mixins.TitleMixin):
    template_name = "core/map/map.html"
    title = "Map"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mapbox_apikey"] = {"apikey": settings.MAPBOX_APIKEY}
        return context


class AboutView(TemplateView, mixins.TitleMixin):
    template_name = "core/about/about.html"
    title = "About"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        members_config = settings.METROPOLIS_STAFFS
        context["members"] = {}
        members_pk_set = set()
        for position in members_config:
            context["members"][position] = models.User.objects.filter(
                pk__in=members_config[position]
            ).order_by("last_name", "first_name")
            members_pk_set.update(members_config[position])
        context["member_count"] = len(members_pk_set)
        return context


class Teapot(View):
    def get(self, request):
        return HttpResponse("orz teapot", status=418)


class Justinian(View):
    def get(self, request):
        return HttpResponse(
            "orz our exalted leader justinian luxtel, waba skyflarus, as payment for his services<br>"
            + gs.justinian_slam(),
            status=402,
        )
