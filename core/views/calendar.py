from django.views.generic import TemplateView

class CalendarView(TemplateView):
    template_name = "core/calendar/view.html"
