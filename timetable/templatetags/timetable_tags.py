from django import template
from django.utils.safestring import mark_safe
from courseshare.settings import TIMETABLE_FORMATS
from django.urls import reverse
 
register = template.Library()
 
@register.filter
def render_timetable(timetable):
    timetable_format = timetable.term.timetable_format
    timetable_config = TIMETABLE_FORMATS[timetable_format]
    courses = {}
    for i in timetable.courses.all():
        courses[i.position] = i
    html = '<table class="table"><thead><tr><th scope="col">Period</th>'
    for i in range(1, timetable_config['days']+1):
        html += f'<th scope="col">Day {i}</th>'
    html += '</tr></thead><tbody>'
    for i in timetable_config['schedule']:
        html += '<tr>'
        html += f'<th scope="row">{i["info"]}</th>'
        for j in i['position']:
            print(courses.keys())
            course_possibilities = j.intersection(courses.keys())
            if len(course_possibilities) > 0:
                course_id = list(course_possibilities)[0]
                course_url = reverse('view_course', args=[courses[course_id].pk, timetable.term.pk])
                html += f'<td><a href="{course_url}">{courses[course_id]}</a></td>'
            else:
                html += f'<td>-</td>'
        html += '</tr>'
    html += '</tbody></table>'
    return mark_safe(html)
