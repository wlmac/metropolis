from django import template
from django.utils.safestring import mark_safe
from metropolis.settings import TIMETABLE_FORMATS
 
register = template.Library()
 
@register.filter
def render_timetable(timetable):
    timetable_format = timetable.term.timetable_format
    timetable_config = TIMETABLE_FORMATS[timetable_format]
    day = timetable.term.day_num()
    courses = {}
    for i in timetable.courses.all():
        courses[i.position] = i
    html = '<table class="table"><thead><tr><th scope="col">Period</th>'
    for i in range(1, timetable_config['cycle']['length']+1):
        if day == i: color = 'table-primary'
        else: color = ''
        html += f'<th scope="col" class="{color}">{timetable_config["cycle"]["duration"].title()} {i}</th>'
    html += '</tr></thead><tbody>'
    for i in timetable_config['schedules'][timetable.term.day_schedule_format()]:
        html += '<tr>'
        html += f'<th scope="row">{i["description"]["time"].lower()}</th>'
        for j in range(0, len(i['position'])):
            if day == j+1: color = 'table-primary'
            else: color = ''
            course_possibilities = i['position'][j].intersection(courses.keys())
            if len(course_possibilities) > 0:
                course_id = list(course_possibilities)[0]
                html += f'<td class="{color}">{courses[course_id]}</td>'
            else:
                html += f'<td class="{color}">-</td>'
        html += '</tr>'
    html += '</tbody></table>'
    return mark_safe(html)
