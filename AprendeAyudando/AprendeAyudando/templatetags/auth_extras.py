from django import template
from django.contrib.auth.models import Group, User

#Constantes
COURSE = 'curso'
ACTIVITY = 'actividad'

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

@register.filter(name='is_owner')
def is_owner(user, request_user):
    return True if user==request_user else False

@register.filter(name='get_item_from_index')
def get_list_items_card(list, quiz_id):
    return list[quiz_id]

@register.filter(name='get_user_from_id')
def get_user_from_id(querySet_of_users, user_id):
    return querySet_of_users.get(id=user_id)

@register.filter(name='get_item_from_dict')
def get_item_from_dict(item, dictt):
    return dictt[item]
    
@register.filter(name='get_first_item_from_dict')
def get_first_item_from_dict(dictt):
    return list(dictt.keys())[0]

@register.filter(name='get_first_value_item_from_dict')
def get_first_value_item_from_dict(dictt):
    return list(dictt.values())[0]