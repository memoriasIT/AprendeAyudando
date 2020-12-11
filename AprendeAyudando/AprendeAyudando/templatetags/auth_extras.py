from django import template
from django.contrib.auth.models import Group 

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    try:
        group = Group.objects.get(name=group_name)
        return True if group in user.groups.all() else False
    except Group.DoesNotExist:
        return False

@register.filter(name='is_guest')
def is_guest(user):
    return not user.is_authenticated
    
@register.filter(name='isCourseOwner')
def isCourseOwner(user, request_user):
    return True if user==request_user else False