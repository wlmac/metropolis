import datetime

from django.utils import timezone


def parse_date_query_param(request):
    date_query_param = request.query_params.get("date")

    if date_query_param == None:
        return timezone.localdate()
    else:
        try:
            return datetime.datetime.strptime(date_query_param, "%Y-%m-%d").date()
        except ValueError:
            return None
