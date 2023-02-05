import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic.base import RedirectView

from .. import models


class RaffleRedirect(LoginRequiredMixin, RedirectView):
    permanent = False
    query_string = False

    def get_redirect_url(self, *args, **kwargs):
        rid = self.request.GET["r"]
        code = self.request.GET["c"]

        raffle = get_object_or_404(models.Raffle, pk=rid)
        uid = self.request.user.id
        raffle.log = raffle.log or "" + json.dumps([uid, code])
        raffle.save()

        # check openness
        now = timezone.now()
        if raffle.open_start > now:
            return HttpResponse("raffle not started yet", status=422)
        if raffle.open_end < now:
            return HttpResponse("raffle already ended", status=422)

        if code in raffle.codes_win:
            return raffle.page_win
        else:
            return raffle.page_lose
