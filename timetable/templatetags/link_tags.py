from django import template
from django.utils.safestring import mark_safe
from django.shortcuts import reverse
 
register = template.Library()
 
@register.filter
def user_url(username):
    return reverse('profile_detail', args=[username])
 
@register.filter
def user(username, postfix=''):
    url = user_url(username)
    return mark_safe('<a href="{0}{1}">{2}</a>'.format(url, postfix, username))

@register.filter
def users(usernames, postfix=''):
    users_string = ""
    for username in usernames:
        users_string += user(username, postfix) + ", "
    return mark_safe(users_string[:-2])
