from datetime import date

from django import template
from django.utils.html import format_html, format_html_join

from core.utils import generic_day_schedule

register = template.Library()


@register.filter
def render_timetable(timetable):
    schedule = generic_day_schedule(date(2000, 1, 1), user=timetable.owner)["schedule"]
    html = format_html(
        '<table class="table"><thead><tr><th scope="col">Period</th>{}</tr></thead><tbody>{}</tbody></table>',
        format_html_join(
            "",
            '<th scope="col">{} {}</th>',
            (("Day", cycle + 1) for cycle in range(2)),
        ),
        format_html_join(
            "",
            '<tr><th scope="row">{}</th>{}</tr>',
            (
                (
                    course["description"]["time"].lower(),
                    format_html_join(
                        "",
                        "<td>{}</td>",
                        (
                            (
                                (
                                    schedule[
                                        (
                                            # this code mogs
                                            period
                                            if not (day == 2 and period in [3, 4])
                                            else 4
                                            if (day, period) == (2, 3)
                                            else 3
                                        )
                                        - 1
                                    ]["description"]["course"]
                                ),
                            )
                            for day in range(1, 3)
                        ),
                    ),
                )
                for period, course in enumerate(schedule, start=1)
            ),
        ),
    )

    return html
