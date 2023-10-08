from django import template
from django.contrib.auth.models import Group



register = template.Library()

@register.filter(name="has_group2")
def has_group2(user, Seeker):
    group = Group.objects.get(name=Seeker)
    return True if group in user.groups.all() else False

@register.filter(name="has_group1")
def has_group1(user, Jobless):
    group = Group.objects.get(name=Jobless)
    return True if group in user.groups.all() else False




