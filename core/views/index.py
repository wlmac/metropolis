from django.conf import settings
from django.urls import reverse
from django_ical.views import ICalFeed
from django.http import HttpResponse
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView

from core.utils import generate_slam as gs
from core.utils import get_week_schedule_info

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
            end_date__gte=datetime_now
        ).order_by("start_date")[:3]

        context["blogpost"] = models.BlogPost.objects.filter(is_published=True).first()

        context["banner_data"] = get_week_schedule_info(self.request.user)
        return context


class CalendarView(TemplateView, mixins.TitleMixin):
    template_name = "core/calendar/view.html"
    title = "Calendar"


class CalendarFeed(ICalFeed):
    product_id = "-//maclyonsden.com//calendar//EN"
    timezone = "UTC"
    file_name = "metropolis_school-wide.ics"

    def items(self):
        now = timezone.now()
        padding = settings.ICAL_PADDING
        return models.Event.get_events(user=None).filter(
            end_date__gte=now - padding, start_date__lte=now + padding,
        ).order_by('-start_date')

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description

    def _is_hms(self, dt, hour, minute, second):
        return dt.hour == hour and dt.minute == minute and dt.second == second

    def item_start_datetime(self, item):
        return item.start_date if self._is_hms(item.start_date, 0, 0, 0) else item.start_date.date()

    def item_end_datetime(self, item):
        return item.end_date if self._is_hms(item.end_date, 23, 59, 0) else item.end_date.date()

    def item_link(self, item):
        # TODO: implement by-pk link
        return reverse("calendar") + f"?pk={item.pk}"  # NOTE: workaround for UID

    def item_categories(self, item):
        return [tag.name for tag in item.tags.all()] \
            + (["public"] if item.is_public else []) \
            + (["instructional"] if item.is_instructional else [])

    def item_author_name(self, item):
        return item.organization.name



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
