from django import template
from django.utils.html import format_html, format_html_join

from core.utils import get_day_schedule

register = template.Library()


@register.filter
def render_timetable(timetable):
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
                    schedule["description"]["time"].lower(),
                    format_html_join(
                        "",
                        "<td>{}</td>",
                        (
                            (
                                (
                                    timetable.courses_str[
                                        (
                                            # this code mogs
                                            period
                                            if not (day == 2 and period in [3, 4])
                                            else 4
                                            if (day, period) == (2, 3)
                                            else 3
                                        )
                                        - 1
                                    ]
                                ),
                            )
                            for day in range(1, 3)
                        ),
                    ),
                )
                for period, schedule in enumerate(
                    get_day_schedule(None, timetable.owner)["schedule"], start=1
                )
            ),
        ),
    )

    return html
