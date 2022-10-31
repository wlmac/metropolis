from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic.base import RedirectView

from .. import models
from . import mixins


class RaffleRedirect(LoginRequiredMixin, RedirectView):
    permanent = False
    query_string = False

    def get_redirect_url(self, *args, **kwargs):
        rid = self.request.GET['r']
        raffle = get_object_or_404(models.Raffle, pk=rid)
        now = timezone.now()
        if raffle.open_start > now:
            raise Http404('s')
        if raffle.open_end < now:
            raise Http404('e')
        code = self.request.GET['c']
        if code in raffle.codes_win:
            return raffle.page_win
        else:
            return raffle.page_lose
