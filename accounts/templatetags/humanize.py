from django import template
from django.utils.timesince import timesince
from django.utils.timezone import now

register = template.Library()

@register.filter
def natural_time(value):
    time_diff = timesince(value, now())
    print(time_diff)
    parts = time_diff.split('，')
    print(parts)
    if len(parts) > 1:
        return f'{parts[0]}前'
    else:
        return f'{time_diff}前'

