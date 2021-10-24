from django import template
from django.conf import settings
from django.utils.html import format_html, format_html_join

register = template.Library()


@register.filter
def render_timetable(timetable):
    timetable_format = timetable.term.timetable_format
    timetable_config = settings.TIMETABLE_FORMATS[timetable_format]

    courses = {}
    for i in timetable.courses.all():
        courses[i.position] = i

    html = format_html(
        '<table class="table"><thead><tr><th scope="col">Period</th>{}</tr></thead><tbody>{}</tbody></table>',
        format_html_join(
            "",
            '<th scope="col">{} {}</th>',
            (
                (timetable_config["cycle"]["duration"].title(), schedule_cycle)
                for schedule_cycle in range(1, timetable_config["cycle"]["length"] + 1)
            ),
        ),
        format_html_join(
            "",
            '<tr><th scope="row">{}</th>{}</tr>',
            (
                (
                    schedule_day["description"]["time"].lower(),
                    format_html_join(
                        "",
                        "<td>{}</td>",
                        (
                            (
                                courses[position_day.intersection(courses.keys()).pop()]
                                if position_day.intersection(courses.keys())
                                else "-",
                            )
                            for position_day in schedule_day["position"]
                        ),
                    ),
                )
                for schedule_day in timetable_config["schedules"][
                    timetable.term.day_schedule_format()
                ]
            ),
        ),
    )

    return html
