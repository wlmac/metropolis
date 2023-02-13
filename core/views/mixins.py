from django.views.generic.base import ContextMixin


class TitleMixin(ContextMixin):
    title = ""

    def get_title(self):
        return self.title

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.get_title()
        return context
