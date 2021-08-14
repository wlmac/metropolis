from django.views.generic import DetailView, ListView
from django.views.generic import TemplateView
from .. import models
from . import mixins

class Index(TemplateView, mixins.TitleMixin):
    template_name = 'core/index.html'
    title = 'Dashboard'
