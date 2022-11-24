from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic.base import RedirectView

from .. import models
from . import mixins

import json


class RaffleRedirect(LoginRequiredMixin, RedirectView):
    permanent = False
    query_string = False

    def get_redirect_url(self, *args, **kwargs):
        rid = self.request.GET['r']  # get id (db row) of raffle
        raffle = get_object_or_404(models.Raffle, pk=rid)  # get raffle  data from database

        # keep track of users that scan raffle
        temp_users = [self.request.user.username]
        if raffle.users_log is not None and raffle.users_log:
            temp_users = list(set(json.loads(raffle.users_log) + temp_users))

        raffle.users_log = json.dumps(temp_users, indent=4)
        raffle.codes_win = [raffle.codes_win]
        raffle.save()  # update the list of users
        
        # make sure raffle isnt expired
        now = timezone.now()
        if raffle.open_start > now:
            raise Http404("s")
        if raffle.open_end < now:
            raise Http404("e")

        # check if user won
        code = self.request.GET["c"]
        if code in raffle.codes_win:
            return raffle.page_win
        else:
            return raffle.page_lose
