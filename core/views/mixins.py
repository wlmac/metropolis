from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import ContextMixin


class CaseInsensitiveUsernameMixin:
    """
    Disallow a username with a case-insensitive match of existing usernames.
    Add this mixin to any forms that use the User object
    """

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if (
            get_user_model()
            .objects.filter(username__iexact=username)
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise forms.ValidationError(
                _("The username ‘{}’ is already in use.".format(username))
            )
        return username


class TitleMixin(ContextMixin):
    title = ""

    def get_title(self):
        return self.title

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.get_title()
        return context
