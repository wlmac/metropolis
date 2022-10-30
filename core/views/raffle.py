from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import RedirectView

from .. import models
from . import mixins


class RaffleRedirect(LoginRequiredMixin, RedirectView):
    permanent = False
    query_string = False

    def get_redirect_url(self, *args, **kwargs):
        rid = self.request.GET['r']
        raffle = models.Raffle.get_object_or_404(rid)
        code = self.request.GET['c']
        if code in raffle.codes_win:
            return raffle.page_win
        else:
            return raffle.page_lose
