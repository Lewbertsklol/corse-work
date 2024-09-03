from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def get_task_name(value: str):
    return value.split("::")[1]


@register.filter
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
