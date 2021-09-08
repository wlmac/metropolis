# some_app/views.py
from django.views.generic import TemplateView

class MapView(TemplateView):
    template_name = "core/map/map.html"
    title = 'Map'
